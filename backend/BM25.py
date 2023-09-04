from haystack.nodes import BM25Retriever
from wiki_retriever import WikiDocumentStore


class retriever_BM25(WikiDocumentStore):
    def __init__(self):
        super().__init__()
        self.retriever = BM25Retriever(document_store=self.document_store)

    def retrieve_RAG(self, claim, top_k=5, max_len=250):
        evidence, text, url = self.retrieve_data(claim, top_k)
        while len(evidence) > max_len and top_k > 1:
            top_k -= 1
            evidence, text, url = self.retrieve_data(claim, top_k)
        return evidence, text, url

    def retrieve_data(self, claim, top_k):
        candidate_docs = self.retriever.retrieve(query=claim, top_k=top_k)
        return super().format_docs_str(candidate_docs)

    def delete_database(self):
        super().delete_database()
