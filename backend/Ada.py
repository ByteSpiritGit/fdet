from haystack.nodes import EmbeddingRetriever
from haystack.document_stores import InMemoryDocumentStore
from wiki_retriever import WikiDocumentStore
import os
from dotenv import load_dotenv


class retriever_Ada(WikiDocumentStore):
    def __init__(self):
        super().__init__()
        load_dotenv()
        self.document_store = InMemoryDocumentStore(
            embedding_dim=1024,
            use_gpu=True,
        )
        self.retriever = EmbeddingRetriever(
            document_store=self.document_store,
            batch_size=1024,
            embedding_model="ada",
            api_key=os.getenv("OPENAI_API_KEY"),
            max_seq_len=1024,
        )

    def update_embed(self):
        self.document_store.update_embeddings(self.retriever)

    def retrieve_RAG(self, claim, top_k=3, max_len=150):
        evidence, text, url = self.retrieve_data(claim, top_k)
        while len(evidence) > max_len and top_k > 1:
            top_k -= 1
            evidence, text, url = self.retrieve_data(claim, top_k)
        return evidence, text, url

    def retrieve_data(self, claim, top_k=3):
        candidate_docs = self.retriever.retrieve(query=claim, top_k=top_k)
        return super().format_docs_str(candidate_docs)

    def delete_database(self):
        super().delete_database()
