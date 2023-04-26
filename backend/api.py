import logging
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from BM25 import retriever_BM25
from DPR import retriever_DPR
from Ada import retriever_Ada
from main import Main
from rag import RAG
import asyncio
import nltk
logging.getLogger("haystack").setLevel(logging.CRITICAL)
logging.getLogger("transformers").setLevel(logging.CRITICAL)
logging.getLogger("nltk").setLevel(logging.CRITICAL)

print("Loading server...")


nltk.download('punkt')
Rag = RAG()
app = FastAPI()

# example = "Andrej Babiš said he would not help baltic states and Poland if they were invaded"

@app.get("/backend")
async def root() -> str:
    help_text = "Welcome to the backend! \n\n" \
                "To use the backend, you can use the following endpoints: \n\n" \
                "GET /backend/v1/dummy \n" \
                "GET /backend/v1/eval \n" \
                "GET /backend/v1/eval_debug \n" \
                "GET /backend/v1/eval_fast \n" \
                "GET /backend/rag/dummy \n" \
                "GET /backend/rag/eval \n" \
                "GET /backend/rag/eval_fast \n\n"
    return help_text


# classification with advanced search
@app.get("/backend/v1/dummy")
def dummy():
    response = [{"claim": "Dummy claim", "label" : "REFUTES", "supports" : 0.1457, "refutes" : 0.8543, "nei": 0.004, "ei": 0.0005, "evidence" : "Lorem ipsum dolor sit amet consectetur adipisicing elit. Totam quibusdam architecto velit ut distinctio culpa possimus, debitis corporis, at officiis voluptas ea modi magni omnis saepe earum! Ullam, velit recusandae. Ipsa quibusdam delectus, debitis quam quisquam quasi consectetur ab obcaecati incidunt amet labore, earum velit modi fuga ducimus dignissimos perspiciatis!"}]
    return JSONResponse(content=response)

@app.get("/backend/v1/eval")
def eval(text: str):
    # response = await validation.main(text) 
    # return JSONResponse(content=response)
    return "Out of service."

@app.get("/backend/v1/eval_debug")
def eval(text: str):
    # response = await validation.main_debug(text) 
    # return JSONResponse(content=response)
    return "Out of service."


@app.get("/backend/v1/eval_fast")
def eval(text: str):
    # response = await validation.main_fast(text) 
    # return JSONResponse(content=response)
    return "Out of service."

# Retrieval-Augmented Generation - RAG
@app.get("/backend/rag/dummy")
def dummy():
    response = [{"claim": "Dummy claim", "label" : "REFUTES", "supports" : 0.1457, "refutes" : 0.8543, "nei": 0.004, "evidence" : "Lorem ipsum dolor sit amet consectetur adipisicing elit. Totam quibusdam architecto velit ut distinctio culpa possimus, debitis corporis, at officiis voluptas ea modi magni omnis saepe earum! Ullam, velit recusandae. Ipsa quibusdam delectus, debitis quam quisquam quasi consectetur ab obcaecati incidunt amet labore, earum velit modi fuga ducimus dignissimos perspiciatis!", "justify" : "Lorem ipsum dolor sit amet consectetur adipisicing elit. Totam quibusdam architecto velit ut distinctio culpa possimus, debitis corporis, at officiis voluptas ea modi magni omnis saepe earum! Ullam, velit recusandae. Ipsa quibusdam delectus, debitis quam quisquam quasi consectetur ab obcaecati incidunt amet labore, earum velit modi fuga ducimus dignissimos perspiciatis!"}]
    return JSONResponse(content=response)

DPR = retriever_DPR()
@app.get("/backend/rag/eval_DPR")
def eval(text: str):
    DPR.create_database(text)
    DPR.update_embed()
    data = DPR.retrieve_RAG(text)
    response =  Rag.main(text, data)
    return JSONResponse(content=response)

@app.get("/backend/rag/eval_ada")
def eval(text: str):
    ADA = retriever_Ada()
    ADA.create_database(text)
    data = ADA.retrieve_RAG(text)
    response = Rag.main(text, data)
    return JSONResponse(content=response)

@app.get("/backend/rag/eval_bm25")
def eval(text: str):
    BM25 = retriever_BM25()
    BM25.create_database(text)
    data = BM25.retrieve_RAG(text)
    response = Rag.main(text, data)
    return JSONResponse(content=response)

if __name__ == "__main__":
    uvicorn.run(app, port=8002)