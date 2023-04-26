from haystack.nodes import EmbeddingRetriever
from haystack.document_stores import InMemoryDocumentStore
from retriever import wiki_document_store
import os
from dotenv import load_dotenv

class retriever_Ada(wiki_document_store):
    def __init__(self):
        super().__init__()
        load_dotenv()
        self.retriever = EmbeddingRetriever(
           document_store=self.document_store,
           batch_size=32,
           embedding_model="ada",
           api_key=os.getenv("OPENAI_API_KEY"),
           max_seq_len=1024
        )

    def update_embed(self):
        self.document_store.update_embeddings(self.retriever)

    def retrieve_RAG(self,claim, top_k=3, max_len=200) -> str:
      evidence, text, url = self.retrieve(claim, top_k)
      while len(evidence[0]) > max_len and top_k > 1:
          top_k -= 1
          evidence, text, url = self.retrieve(claim, top_k)
      return evidence, text, url

    def retrieve(self, query, top_k):
        candidate_docs = self.retriever.retrieve(query=query, top_k=top_k)
        return super().format_docs_str(candidate_docs)
    
    def delete_database(self, documents):
        super().delete_database(documents)
