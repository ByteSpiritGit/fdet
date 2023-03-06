from wikipedia import Wikipedia
from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import DensePassageRetriever
from yake import KeywordExtractor
import asyncio
import re

class TextRetrieverV2():
    def __init__(self) -> None:
        self.wiki = Wikipedia("en")
        self.kw_extractor = KeywordExtractor()
        self.document_store = InMemoryDocumentStore(embedding_dim=768, use_gpu=True)
        self.loop = asyncio.get_event_loop()
        self.retriever = DensePassageRetriever(
        document_store=self.document_store,
        query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
        passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
        use_gpu=True,
        use_fast_tokenizers=True
        )

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
            sentences = []
            text =  i[1].split('.')
            for line in text:
                sentences.append(line)
            for num, line in enumerate(sentences):
                dicts.append(
                {
                'content': line,
                'meta': {'title': i[0], "ID" : num}
                }
                )
        self.document_store.write_documents(dicts)
        self.document_store.update_embeddings(self.retriever)
        return self.document_store

    def extract_passage(self, claim, top_k):
        candidate_documents = self.retriever.retrieve(
            query=claim,
            top_k=top_k
        )
        evidence = ""
        for i in candidate_documents:
            content = i.content.replace('\n', '')
            content = re.sub("since (\d+)", r"since \1 to 2023", content)
            evidence += f"{content}\n"
        evidence = evidence.replace("–present", "-2023")
        return evidence
    
    def create_database(self, text) -> bool:
        # Example usage
        keyWords = self.__extractKeyWords(text)
        pages = self.loop.run_until_complete(self.__extract_wikipedia_pages(keyWords))
        self.__storeDocuments(pages)
        return True

    def delete_database(self) -> bool:
        self.document_store.delete_documents()
        return True
    