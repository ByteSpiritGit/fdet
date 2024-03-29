import logging
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from BM25 import retriever_BM25
from DPR import retriever_DPR
from Ada import retriever_Ada
from rag_gpt3 import GPT3
from datetime import datetime
import threading
import nltk
from fastapi.middleware.cors import CORSMiddleware

logging.getLogger("haystack").setLevel(logging.CRITICAL)
logging.getLogger("transformers").setLevel(logging.CRITICAL)
logging.getLogger("nltk").setLevel(logging.CRITICAL)
logging.getLogger()

logger = logging.getLogger(__name__)

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
lock = threading.Lock()

N_BM25 = 0
N_DPR = 1
N_ADA = 0

logger.info(datetime.now().strftime("%H:%M:%S") + " - Loading retrievers...[BM25, DPR, Ada]")
logger.info(datetime.now().strftime("%H:%M:%S") + " - Loading BM25... [1/3]")
BM25_instances = [retriever_BM25() for i in range(N_BM25)]
in_use_BM25 = set()

logging.info(datetime.now().strftime("%H:%M:%S") + " - Loading DPR... [2/3]")
DPR_instances = [retriever_DPR() for j in range(N_DPR)]
in_use_DPR = set()

logger.info(datetime.now().strftime("%H:%M:%S") + " - Loading ADA... [3/3]")
ADA_instances = [retriever_Ada() for k in range(N_ADA)]
in_use_ADA = set()

logger.info(datetime.now().strftime("%H:%M:%S") + " - Loading RAG...")
RAG_instance = GPT3()

logger.info(datetime.now().strftime("%H:%M:%S") + " - Loading server...")
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def eval_fnc_emb(retriever_instances, in_use, calc_instance, text: str) -> JSONResponse:
    with lock:
        retriever = None
        for instance in retriever_instances:
            if instance not in in_use:
                retriever = instance
                in_use.add(instance)
                break
        if retriever is None:
            return JSONResponse(status_code=503, content={"message": "All instances are in use"})
    try:
        retriever.create_database(text)
        retriever.update_embed()
        response = calc_instance.main(text, retriever)
        retriever.delete_database()
        with lock:
            in_use.remove(retriever)
        return JSONResponse(content=response)
    except Exception as Error:
        logger.error(Error)
        with lock:
            in_use.remove(retriever)
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})


# TODO: repair main function Error in retriever in main
def eval_fnc(retriever_instances, in_use, calc_instance, text: str) -> JSONResponse:
    with lock:
        retriever = None
        for instance in retriever_instances:
            if instance not in in_use:
                retriever = instance
                in_use.add(instance)
                break
        if retriever is None:
            return JSONResponse(status_code=503, content={"message": "All instances are in use"})
    try:
        retriever.create_database(text)
        response = calc_instance.main(text, retriever)
        retriever.delete_database()
        with lock:
            in_use.remove(retriever)
        return JSONResponse(content=response)
    except Exception as Error:
        logger.error(Error)
        with lock:
            in_use.remove(retriever)
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})


# Retrieval-Augmented Generation - RAG
@app.get("/backend/rag/dummy")
def dummy():
    response = [{"claim": "Dummy claim", "label": "REFUTES", "supports": 0.1457, "refutes": 0.8543, "nei": 0.004,
                 "evidence": ["Lorem ipsum dolor sit amet consectetur adipisicing elit.",
                              "Totam quibusdam architecto velit ut distinctio culpa possimus, debitis corporis, "
                              "at officiis voluptas ea modi magni omnis saepe earum !",
                              "Ullam, velit recusandae.",
                              "Ipsa quibusdam delectus, debitis quam quisquam quasi consectetur ab obcaecati "
                              "incidunt amet labore, earum velit modi fuga ducimus dignissimos perspiciatis!"],
                 "justify": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Totam quibusdam architecto"
                            " velit ut distinctio culpa possimus, debitis corporis, at officiis voluptas ea modi"
                            " magni omnis saepe earum! Ullam, velit recusandae. Ipsa quibusdam delectus, debitis quam"
                            " quisquam quasi consectetur ab obcaecati incidunt amet labore, earum velit"
                            " modi fuga ducimus dignissimos perspiciatis!",
                 "url": ["https://www.google.com", "https://www.google.com", "https://www.google.com",
                         "https://www.google.com"]}]
    return JSONResponse(content=response)


@app.get("/backend/rag/eval_dpr")
def eval_dpr(text: str):
    return eval_fnc_emb(DPR_instances, in_use_DPR, RAG_instance, text)


@app.get("/backend/rag/eval_ada")
def eval_ada(text: str):
    return eval_fnc_emb(ADA_instances, in_use_ADA, RAG_instance, text)


@app.get("/backend/rag/eval_bm25")
def eval_bm25(text: str):
    return eval_fnc(BM25_instances, in_use_BM25, RAG_instance, text)


@app.get("/coffee")
async def root():
    return JSONResponse(status_code=418, content={"message": "I'm a teapot"})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
