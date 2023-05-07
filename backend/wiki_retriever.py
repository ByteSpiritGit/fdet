import nltk
from wikipedia import Wikipedia
from haystack.utils import clean_wiki_text
from haystack.document_stores import InMemoryDocumentStore
from yake import KeywordExtractor
import asyncio
import re
import nltk
import math
from collections import Counter
from nltk.tokenize import word_tokenize
from datetime import datetime
from google_api import googleAPI

class wiki_document_store():
    def __init__(self) -> None:
        self.STOP_WORDS = ["a", "an", "the", "o"]
        self.wiki = Wikipedia("en")
        self.kw_extractor = KeywordExtractor()
        self.document_store = InMemoryDocumentStore(
            use_bm25= True,
            use_gpu=True
        )
        self.WORD = re.compile(r'\w+')
        self.google_api = googleAPI()


    def get_cosine(self, vec1, vec2) -> float:
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum(vec1[x] * vec2[x] for x in intersection)
        sum1 = math.fsum(vec1[x]**2 for x in vec1)
        sum2 = math.fsum(vec2[x]**2 for x in vec2)
        denominator = math.sqrt(sum1) * math.sqrt(sum2)
        return float(numerator) / denominator if denominator else 0.0
    
    def text_to_vector(self, text) -> Counter:
        return Counter(self.WORD.findall(text.lower()))
    
    def get_text_similarity(self, a, b) -> float:
        a = self.text_to_vector(a.strip())
        b = self.text_to_vector(b.strip())
        return self.get_cosine(a, b)

    def __extractKeyWords(self, text, keyWords=3) -> list:
        words = word_tokenize(text)
        pos = nltk.pos_tag(words)
        nouns = [word for word, tag in pos if tag.startswith('N')]
        nouns += [word for word, tag in pos if tag == 'PRP']
        # Extract Subject
        temp_titles = self.kw_extractor.extract_keywords(text)
        temp_titles = [(tup[0], tup[1]+self.get_text_similarity(text, tup[0])) if tup[0] in nouns else tup for tup in temp_titles]
        temp_titles = self.add_value_from_substring(temp_titles)
        temp_titles = sorted(temp_titles, key=lambda x: x[1], reverse=True)
        pages = [i[0] for i in temp_titles]
        return pages[:keyWords]   
    
    def add_value_from_substring(self, lst):
        for i in range(len(lst)):
            for j in range(len(lst)):
                if i != j and lst[j][0] in lst[i][0] and (len(lst[i][0]) > len(lst[j][0])):
                    lst[i] = (lst[i][0], lst[i][1]+lst[j][1])
        return lst

    def remove_stop_words(self, text):
        text = text.split()
        text = " ".join([i for i in text if i not in self.STOP_WORDS])
        return text

    async def __fetch_wikipedia_page(self, title):
        wikiPages = self.wiki.search(title)
        page = None
        
        if wikiPages == []: 
            wikiPages = self.wiki.search("Rickrolling")
        
        for i in wikiPages:
            if i[0].lower() == title.lower():
                page = i
                break
        if len(wikiPages) > 0 and page != None:
            return (page[0] ,self.wiki.extract_page(title=page[0]))
        return (wikiPages[0], self.wiki.extract_page(title=wikiPages[0]), self.wiki.open_search(title=wikiPages[0])[0   ][1])

    async def __extract_wikipedia_pages(self, titles):
        tasks = [self.__fetch_wikipedia_page(title) for title in titles]
        results = await asyncio.gather(*tasks)
        results = list({tup: None for tup in results})
        return results

    def storeDocuments(self, documents):        
        dicts = []
        for i in documents:    
            text = clean_wiki_text(i[1])
            text = text.split("== References ==")[0].split("== External links ==")[0]
            text = re.sub(r'  ', r' ', text)
            text = re.sub(r'(\n)+', r'\n', text)
            text = nltk.sent_tokenize(text)
            for num, line in enumerate(text):
                dicts.append(
                {
                'content': self.remove_stop_words(line.lower()),
                'meta': {'title': i[0], "ID" : num, 'text': line, 'url': i[2]}
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

    def create_database(self, text, n_pages=3) -> bool:
        keyWords = self.__extractKeyWords(text, n_pages)
        pages = asyncio.run(self.__extract_wikipedia_pages(keyWords))
        pages += self.google_api.main(text)
        self.storeDocuments(pages)
        return self.document_store

    def delete_database(self) -> bool:
        self.document_store.delete_documents()
        return True
    

