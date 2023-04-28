from haystack.nodes import DensePassageRetriever
from wiki_retriever import wiki_document_store
from haystack.document_stores import InMemoryDocumentStore

class retriever_DPR(wiki_document_store):
    def __init__(self):
        super().__init__()
        self.document_store = InMemoryDocumentStore(
           embedding_dim=768,
           use_gpu=True
           )
        self.retriever = DensePassageRetriever(
            document_store=self.document_store,
            query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
            passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
            batch_size=32,
            use_gpu=True,
            use_fast_tokenizers=True
        )

    def create_database(self, text):
      super().create_database(text)
    
    def update_embed(self):
        self.document_store.update_embeddings(self.retriever)

    def retrieve_RAG(self,claim, top_k=3, max_len=125) -> str:
      evidence, text, url = self.retrieve(claim, top_k)
      while len(evidence[0]) > max_len and top_k > 1:
          top_k -= 1
          evidence, text, url = self.retrieve(claim, top_k)
      return evidence, text, url

    def retrieve(self, query, top_k):
      candidate_docs = self.retriever.retrieve(query=query, top_k=top_k)
      return super().format_docs_str(candidate_docs)
    
    def delete_database(self):
      super().delete_database()