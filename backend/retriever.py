import nltk
from wikipedia import Wikipedia
from haystack.utils import clean_wiki_text, convert_files_to_docs, fetch_archive_from_http
from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import DensePassageRetriever, BM25Retriever
from yake import KeywordExtractor
import asyncio
import re
import anlys
import logging
logging.getLogger('nltk').setLevel(logging.CRITICAL)
class TextRetrieverV2():
    def __init__(self) -> None:
        self.wiki = Wikipedia("en")
        self.kw_extractor = KeywordExtractor()
        self.document_store = InMemoryDocumentStore(
            embedding_dim=768,                                       
            use_gpu=True,
            use_bm25= True
        )
        # self.loop = asyncio.get_event_loop()
        self.DPR = DensePassageRetriever(
        document_store=self.document_store,
        query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
        passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
        batch_size=256,
        use_gpu=True,
        use_fast_tokenizers=True
        )
        self.BM25 = BM25Retriever(self.document_store)

    def __extractKeyWords(self, text) -> list:
        # Extract Subject
        pages = []
        for i in text:
            temp_titles = self.kw_extractor.extract_keywords(i)
            for title in temp_titles:
                pages.append(title[0])
        return pages[:5]   


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
        return (wikiPages[0], self.wiki.extract_page(title=wikiPages[0]))

    async def __extract_wikipedia_pages(self, titles):
        tasks = [self.__fetch_wikipedia_page(title) for title in titles]
        results = await asyncio.gather(*tasks)
        results = list({tup: None for tup in results})
        return results

    def __storeDocuments(self, documents):        
        dicts = []
        for i in documents:         
            text = i[1].split("== References ==")[0].split("== External links ==")[0]
            text = re.sub(r'  ', r' ', text)
            text = re.sub(r'(\n)+', r'\n', text)

            text = nltk.sent_tokenize(text)
            for num, line in enumerate(text):
                dicts.append(
                {
                'content': anlys.remove_stop_words(line.lower()),
                'meta': {'title': i[0], "ID" : num, 'text': line}
                }
                )
        self.document_store.write_documents(dicts)
        return self.document_store
    
    def __storeDocuments_DPR(self, documents):
        self.__storeDocuments(documents)
        self.document_store.update_embeddings(self.DPR)
        return self.document_store

    def __storeDocuments_BM25(self, documents):        
        return self.__storeDocuments(documents)

    def __extract_passage_str(self, retriever, claim, top_k) -> str:
        candidate_documents = retriever.retrieve(
            query=claim,
            top_k=top_k
        )
        evidence = ""
        for i in candidate_documents:
            content = i.content.replace('\n', '')
            content = re.sub("since (\d+)", r"since \1 to 2023", content)
            evidence += f"{content}"
        evidence = evidence.replace("–present", "-2023")

        text = ""
        for i in candidate_documents:
            content = i.meta["text"].replace('\n', '')
            content = re.sub("since (\d+)", r"since \1 to 2023", content)
            text += f"{content}"
        text = text.replace("–present", "-2023")
        return evidence, text
    
    def __extract_passage_list(self, retriever, claim, top_k) -> list:
        candidate_documents = retriever.retrieve(
            query=claim,
            top_k=top_k
        )
        evidence = []
        for i in candidate_documents:
            content = i.content.replace('\n', '')
            content = re.sub("since (\d+)", r"since \1 to 2023", content)
            content = content.replace("–present", "-2023")
            evidence.append(content)

        text = []
        for i in candidate_documents:
            content = i.text.replace('\n', '')
            content = re.sub("since (\d+)", r"since \1 to 2023", content)
            content = content.replace("–present", "-2023")
            text.append(content)
        return evidence
    
    def extract_passage_str_DPR(self,claim, top_k) -> str:
        return self.__extract_passage_str(self.DPR, claim, top_k)
    
    def extract_passage_list_DPR(self,claim, top_k) -> list:
        return self.__extract_passage_list(self.DPR, claim, top_k)

    def extract_passage_str_BM25(self,claim, top_k) -> str:
        return self.__extract_passage_str(self.BM25, claim, top_k)

    def extract_passage_list_BM25(self,claim, top_k) -> list:
        return self.__extract_passage_list(self.BM25, claim, top_k)
    
    def extract_passage_str_DPR_RAG(self,claim, top_k=3, max_tokens=350) -> str:
        evidence = self.extract_passage_str_DPR(claim, top_k)
        while len(evidence[0]) > max_tokens and top_k > 1:
            top_k -= 1
            evidence = self.extract_passage_str_DPR(claim, top_k)
        return evidence
    
    async def create_database_DPR(self, text) -> bool:
        keyWords = self.__extractKeyWords(text)
        pages = await self.__extract_wikipedia_pages(keyWords)
        self.__storeDocuments_DPR(pages)
        return True

    async def create_database_BM25(self, text) -> bool:
        keyWords = self.__extractKeyWords(text)
        pages = await self.__extract_wikipedia_pages(keyWords)
        self.__storeDocuments_BM25(pages)
        return True

    def delete_database(self) -> bool:
        self.document_store.delete_documents()
        return True
    