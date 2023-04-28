import logging
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from BM25 import retriever_BM25
from DPR import retriever_DPR
from Ada import retriever_Ada
from main import Main
from rag import RAG
from datetime import datetime
import threading
import nltk

logging.getLogger("haystack").setLevel(logging.CRITICAL)
logging.getLogger("transformers").setLevel(logging.CRITICAL)
logging.getLogger("nltk").setLevel(logging.CRITICAL)
logging.getLogger().setLevel(logging.INFO)


nltk.download('punkt')
lock = threading.Lock()

N_BM25 = 30
N_DPR = 2
N_ADA = 30


logging.info(datetime.now().strftime("%H:%M:%S") + " - Loading retrievers...[BM25, DPR, Ada]")
logging.info(datetime.now().strftime("%H:%M:%S") + " - Loading BM25... [1/3]")
BM25_instances = [retriever_BM25() for i in range(N_BM25)]
in_use_BM25 = set()

logging.info(datetime.now().strftime("%H:%M:%S") + " - Loading DPR... [2/3]")
DPR_instances = [retriever_DPR() for i in range(N_DPR)]
in_use_BM25 = set()

logging.info(datetime.now().strftime("%H:%M:%S") + " - Loading ADA... [3/3]")
ADA_instances = [retriever_Ada() for i in range(N_ADA)]
in_use_ADA = set()

logging.info(datetime.now().strftime("%H:%M:%S") + " - Loading models...[RAG, Main]")
logging.info(datetime.now().strftime("%H:%M:%S") + " - Loading RAG... [1/2]")
RAG_instance = RAG()

logging.info(datetime.now().strftime("%H:%M:%S") + " - Loading Main... [2/2]")
Main_instance = Main()

logging.info(datetime.now().strftime("%H:%M:%S") + " - Loading server...")
app = FastAPI()

@app.get("/backend")
async def root() -> str:
    help_text = "Welcome to the backend of the Fact-Checking System. Please use the following endpoints to access the system: \n" \
                "/backend/v1/dummy \n"  \
                "/backend/v1/eval?text=... \n" \
                "/backend/v1/eval_debug?text=... \n" \
                "/backend/v1/eval_fast?text=... \n" \
                "/backend/rag/dummy \n" \
                "/backend/rag/eval?text=... \n" \
                "/backend/rag/eval_DPR?text=... \n" \
                "/backend/rag/eval_Ada?text=... \n" \
                "/backend/rag/eval_BM25?text=... \n" 
    return help_text


# classification with advanced search
@app.get("/backend/v1/dummy")
def dummy():
    response = [{"claim": "Dummy claim", "label" : "REFUTES", "supports" : 0.1457, "refutes" : 0.8543, "nei": 0.004, "ei": 0.0005, "evidence" : "Lorem ipsum dolor sit amet consectetur adipisicing elit. Totam quibusdam architecto velit ut distinctio culpa possimus, debitis corporis, at officiis voluptas ea modi magni omnis saepe earum! Ullam, velit recusandae. Ipsa quibusdam delectus, debitis quam quisquam quasi consectetur ab obcaecati incidunt amet labore, earum velit modi fuga ducimus dignissimos perspiciatis!"}]
    return JSONResponse(content=response)

@app.get("/backend/v1/eval_DPR")
def eval(text: str):
    with lock:
        DPR = None
        for instance in DPR_instances:
            if instance not in in_use_BM25:
                DPR = instance
                in_use_BM25.add(instance)
                break
        if DPR is None:
            return JSONResponse(status_code=503, content={"message": "All instances are in use"})
    response = Main_instance.main(text, DPR) 
    with lock:
        in_use_BM25.remove(DPR)
    return JSONResponse(content=response)

@app.get("/backend/v1/eval_fast")
def eval(text: str):
    with lock:
        BM25 = None
        for instance in BM25_instances:
            if instance not in in_use_BM25:
                BM25 = instance
                in_use_BM25.add(instance)
                break
        if BM25 is None:
            return JSONResponse(status_code=503, content={"message": "All instances are in use"})
    response = Main_instance.main_debug(text, BM25)
    with lock:
        in_use_BM25.remove(BM25)
    return JSONResponse(content=response)

# Retrieval-Augmented Generation - RAG
@app.get("/backend/rag/dummy")
def dummy():
    response = [{"claim": "Dummy claim", "label" : "REFUTES", "supports" : 0.1457, "refutes" : 0.8543, "nei": 0.004, "evidence" : "Lorem ipsum dolor sit amet consectetur adipisicing elit. Totam quibusdam architecto velit ut distinctio culpa possimus, debitis corporis, at officiis voluptas ea modi magni omnis saepe earum! Ullam, velit recusandae. Ipsa quibusdam delectus, debitis quam quisquam quasi consectetur ab obcaecati incidunt amet labore, earum velit modi fuga ducimus dignissimos perspiciatis!", "justify" : "Lorem ipsum dolor sit amet consectetur adipisicing elit. Totam quibusdam architecto velit ut distinctio culpa possimus, debitis corporis, at officiis voluptas ea modi magni omnis saepe earum! Ullam, velit recusandae. Ipsa quibusdam delectus, debitis quam quisquam quasi consectetur ab obcaecati incidunt amet labore, earum velit modi fuga ducimus dignissimos perspiciatis!"}]
    return JSONResponse(content=response)

@app.get("/backend/rag/eval_DPR")
def eval_DPR(text: str):
    with lock:
        # find an instance that is not in use
        DPR = None
        for instance in DPR_instances:
            if instance not in in_use_BM25:
                DPR = instance
                in_use_BM25.add(instance)
                break
        if DPR is None:
            return JSONResponse(status_code=503, content={"message": "All instances are in use"})
    DPR.create_database(text)
    DPR.update_embed()
    data = DPR.retrieve_RAG(text)
    DPR.delete_database()
    with lock:
        in_use_BM25.remove(DPR)
    response = RAG_instance.main(text, data)
    return JSONResponse(content=response)

@app.get("/backend/rag/eval_ada")
def eval_ada(text: str):
    with lock:
        ADA = None
        for instance in ADA_instances:
            if instance not in in_use_ADA:
                ADA = instance
                in_use_ADA.add(instance)
                break
        if ADA is None:
            return JSONResponse(status_code=503, content={"message": "All instances are in use"})
    ADA.create_database(text)
    ADA.update_embed()
    data = ADA.retrieve_RAG(text)
    ADA.delete_database()
    with lock:
        in_use_ADA.remove(ADA)
    response = RAG_instance.main(text, data)
    return JSONResponse(content=response)

@app.get("/backend/rag/eval_bm25")
def eval_bm25(text: str):
    with lock:
        BM25 = None
        for instance in BM25_instances:
            if instance not in in_use_BM25:
                BM25 = instance
                in_use_BM25.add(instance)
                break
        if BM25 is None:
            return JSONResponse(status_code=503, content={"message": "All instances are in use"})
    data = BM25.retrieve_RAG(text)
    with lock:
        in_use_BM25.remove(BM25)
    response = RAG_instance.main(text, data)
    return JSONResponse(content=response)

if __name__ == "__main__":
    uvicorn.run(app, port=8002)