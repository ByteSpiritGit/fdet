import nltk
from wikipedia import Wikipedia
from haystack.utils import clean_wiki_text
from haystack.document_stores import InMemoryDocumentStore
from yake import KeywordExtractor
import asyncio
import re
import anlys
import logging
from datetime import datetime
class wiki_document_store():
    def __init__(self) -> None:
        self.wiki = Wikipedia("en")
        self.kw_extractor = KeywordExtractor()
        self.document_store = InMemoryDocumentStore(
            use_bm25= True,
            use_gpu=True,
        )

    def __extractKeyWords(self, text, keyWords=3) -> list:
        # Extract Subject
        temp_titles = self.kw_extractor.extract_keywords(text)
        pages = [i[0] for i in temp_titles]
        return pages[:keyWords]   


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

    async def storeDocuments(self, documents):        
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
                'content': anlys.remove_stop_words(line.lower()),
                'meta': {'title': i[0], "ID" : num, 'text': line, 'url': i[2]}
                }
                )
        self.document_store.write_documents(dicts)
        return self.document_store

    def format_docs_str(self, candidate_documents) -> tuple:
        evidence = ""
        text = ""
        url = []
        current_year = datetime.now().year
        for i in candidate_documents:
            content = i.content.replace('\n', '')
            content = re.sub(r"since (\d+)", f"since \\1 to {current_year}", content)
            evidence += f"{content}"
            url.append(i.meta.get("url"))
            content = i.meta["text"].replace('\n', '')
            content = re.sub(r"since (\d+)", f"since \\1 to {current_year}", content)
            text += f"{content}"
        evidence = evidence.replace("–present", "-2023")
        text = text.replace("–present", "-2023")
        return evidence, text, url

    def create_database(self, text) -> bool:
        keyWords = self.__extractKeyWords(text)
        pages = asyncio.run(self.__extract_wikipedia_pages(keyWords))
        asyncio.run(self.storeDocuments(pages))
        return self.document_store

    def delete_database(self) -> bool:
        self.document_store.delete_documents()
        return True
    