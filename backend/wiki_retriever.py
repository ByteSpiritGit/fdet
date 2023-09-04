import asyncio
import re
from datetime import datetime
from typing import List, Dict, Any
from itertools import chain

import torch
import nltk
from nltk.corpus import stopwords
from haystack.document_stores import InMemoryDocumentStore
from haystack.utils import clean_wiki_text
from yake import KeywordExtractor
from transformers import AutoModel, AutoTokenizer, AutoModelForTokenClassification, pipeline

from wikipedia import Wikipedia


class WikiDocumentStore():
    def __init__(self, embedding_model_name="sentence-transformers/all-MiniLM-L6-v2",
                 ner_model_name="51la5/roberta-large-NER"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        ner_model = AutoModelForTokenClassification.from_pretrained(ner_model_name).to(self.device)
        ner_model = ner_model.half()
        ner_tokenizer = AutoTokenizer.from_pretrained(ner_model_name, model_max_length=512)
        ner_model.eval()
        self.ner_pipeline = pipeline("token-classification",model=ner_model, tokenizer=ner_tokenizer,
                                     framework="pt", device=self.device)

        embed_model = AutoModel.from_pretrained(embedding_model_name).to(self.device)
        self.embed_model = embed_model.half()
        self.embed_tokenizer = AutoTokenizer.from_pretrained(embedding_model_name, model_max_length=512)
        self.embed_model.eval()

        nltk.download('stopwords')
        self.wiki = Wikipedia("en")
        self.kw_extractor = KeywordExtractor()
        self.document_store = InMemoryDocumentStore(
            use_bm25=True,
            use_gpu=True
        )

    def get_cosine(self, tensor1: torch.Tensor, tensor2: torch.Tensor) -> float:
        return torch.nn.functional.cosine_similarity(tensor1, tensor2, dim=1).item()

    def text_to_vector(self, text):
        text_tokenized = self.embed_tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512).to(self.device)
        with torch.no_grad():
            model_output = self.embed_model(**text_tokenized)
        embeddings = model_output.last_hidden_state[:, 0, :]
        return embeddings

    def get_text_similarity(self, a: str, b: str) -> float:
        vec1 = self.text_to_vector(a)
        vec2 = self.text_to_vector(b)
        return self.get_cosine(vec1, vec2)

    def __get_ner(self, text: str) -> list:
        """
        Extract named entities from a given text.
        :param text: The input text.
        :return: The list of named entities. with score
        {{"entity": "I-LOC", "word": "Germany", "score": 0.99}
        """
        entities = self.ner_pipeline(text)
        # Initialize variables for grouping
        grouped_entities = []
        current_group = []

        def create_record(group: list):
            return {'entity': group[0]['entity'],
                    'word': ''.join([e['word'] for e in group]).replace("▁", " ").strip(),
                    'score': sum([e['score'] for e in group]) / len(group)}


        # Iterate through the sorted data to group consecutive entities with the same entity type
        for entry in entities:
            if not current_group or (entry['entity'] == current_group[0]['entity'] and entry['index'] == current_group[0]['index'] + 1):
                current_group.append(entry)
            else:
                # If the entity type changes, add the previous group to the result and start a new group
                grouped_entities.append(create_record(current_group))
                current_group = [entry]

        # Add the last group to the result
        if current_group:
            grouped_entities.append(create_record(current_group))

        return grouped_entities

    def __extract_key_words(self, text: str, n_keywords=3) -> list:
        """
        Extract keywords from a given text.
        :param text: The input text.
        :param n_keywords: The number of keywords to extract.
        :return:
        list: The list of keywords.
        """
        keywords = {}
        # Get named entities
        entities = self.__get_ner(text)

        if not entities:
            keywords = self.kw_extractor.extract_keywords(text)
        elif entities:
            # Add named entities to keywords
            for i in entities:
                if i["entity"] in keywords:
                    keywords[i["word"]] += i["score"]
                else:
                    keywords[i["word"]] = i["score"]

        # Sort keywords by score
        sorted_keywords = dict(sorted(keywords.items(), key=lambda item: item[1], reverse=True))
        return list(sorted_keywords.keys())[:n_keywords]

    def remove_stopwords(self, text, language='english'):
        """
        Remove stop words from a given text.
        :param text: The input text.
        :return: str: The input text with stop words removed.
        """
        stop_words = set(stopwords.words(language))
        words = text.split()
        filtered_words = [word for word in words if word.lower() not in stop_words]
        return ' '.join(filtered_words)

    async def __fetch_wikipedia_snippet(self, title) -> List[Dict[str, str]]:
        return self.wiki.search(title)

    async def __extract_wikipedia_snippets(self, titles):
        """
        Fetch a wikipedia page.
        :param titles:
        :return 1dim list of dicts:
        """
        tasks = [self.__fetch_wikipedia_snippet(title) for title in titles]
        results = await asyncio.gather(*tasks)
        return results

    def __score_snippets(self, text: str, title_snippet_list: List[Dict[str, str]], n_titles=1) -> list[
        dict[str, str | float]]:
        """
        Choose the most relevant keyword and snipet from a list of titles and snipets.
        :param text: The input text.
        :param title_snippet_list: The list of titles and snipets.
        :return: The most relevant keyword and snipet.
        """
        title_snippet_list = [item for item in title_snippet_list if item["snippet"]]
        scored_list = [{"title": item["title"], "score": self.get_text_similarity(text, item["snippet"])} for item in
                       title_snippet_list]

        scored_list = [item for item in scored_list if item["score"]]

        sorted_scored_list = sorted(scored_list, key=lambda x: x["score"], reverse=True)
        # return n titles
        return sorted_scored_list[:n_titles]

    def __choose_wiki_page(self, text: str, keywords: List[str], n_pages=1) -> list[str]:
        """
        Choose the most relevant wikipedia page from a list of keywords.
        :param text: The input text.
        :param keywords: The list of keywords.
        :return: The most relevant wikipedia page.
        """
        # Fetch snipets from wikipedia
        snippet_list = asyncio.run(self.__extract_wikipedia_snippets(keywords))
        # Choose the most relevant keyword and snipet
        scored_snippet = list(chain.from_iterable(self.__score_snippets(text, item_list, n_pages) for item_list in snippet_list))
        # return n titles
        return scored_snippet[:n_pages]

    async def __fetch_wikipedia_page(self, keyword):
        return {"title": keyword['title'], "page_text": self.wiki.extract_page(title=keyword["title"]),"url": f"{self.wiki.wiki_url}/{keyword['title'].replace(' ', '_')}"}

    async def __extract_wikipedia_pages(self, titles):
        tasks = [self.__fetch_wikipedia_page(title) for title in titles]
        results = await asyncio.gather(*tasks)
        return results

    def store_documents(self, documents):
        """
        Store documents in the document store.
        """
        dicts = []
        for i in documents:
            text = clean_wiki_text(i["page_text"])
            text = text.split("== References ==")[0].split("== External links ==")[0]
            text = re.sub(r'  ', r' ', text)
            text = re.sub(r'(\n)+', r'\n', text)
            text = nltk.sent_tokenize(text)
            for num, line in enumerate(text):
                dicts.append(
                    {
                        'content': self.remove_stopwords(line.lower()),
                        'meta': {'keyword': i["title"], "ID": num, 'text': line, 'url': i["url"]}
                    }
                )
        self.document_store.write_documents(dicts)
        return self.document_store

    def format_docs_str(self, candidate_documents) -> tuple:
        evidence = ""
        text = []
        url = []
        current_year = datetime.now().year
        for i in candidate_documents:
            content = i.content.replace('\n', '')
            content = re.sub(r"since (\d+)", f"since \\1 to {current_year}", content)
            evidence += f"{content}"
            url.append(i.meta.get("url"))
            content = i.meta["text"].replace('\n', '')
            content = re.sub(r"since (\d+)", f"since \\1 to {current_year}", content)
            content = content.replace("–present", "-2023")
            text.append(content)
        evidence = evidence.replace("–present", "-2023")
        return evidence, text, url

    def create_database(self, text, n_keywords=3, n_pages=3):
        """
        Create a database of documents from a given text via wiki.
        :param text: The input text.
        :param n_keywords: The number of keywords to extract.
        :param n_pages: The number of pages to extract.
        """
        keywords = self.__extract_key_words(text, n_keywords)
        pages_titles = self.__choose_wiki_page(text, keywords, n_pages)
        pages = asyncio.run(self.__extract_wikipedia_pages(pages_titles))
        self.store_documents(pages)

    def delete_database(self) -> bool:
        self.document_store.delete_documents()
        return True


if __name__ == "__main__":
    wiki = WikiDocumentStore()
    wiki.create_database("The first president of the United States was George Washington.")

