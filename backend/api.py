import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from main import main
from rag import RAG

app = FastAPI()
validation = main()
rag = RAG()

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
                "GET /backend/rag/eval \n"
    return help_text


# classification with advanced search
@app.get("/backend/v1/dummy")
async def dummy():
    response = [{"claim": "Dummy claim", "label" : "REFUTES", "supports" : 0.1457, "refutes" : 0.8543, "nei": 0.004, "ei": 0.0005, "evidence" : "Lorem ipsum dolor sit amet consectetur adipisicing elit. Totam quibusdam architecto velit ut distinctio culpa possimus, debitis corporis, at officiis voluptas ea modi magni omnis saepe earum! Ullam, velit recusandae. Ipsa quibusdam delectus, debitis quam quisquam quasi consectetur ab obcaecati incidunt amet labore, earum velit modi fuga ducimus dignissimos perspiciatis!"}]
    return JSONResponse(content=response)

@app.get("/backend/v1/eval")
async def eval(text: str):
    response = await validation.main(text) 
    return JSONResponse(content=response)

@app.get("/backend/v1/eval_debug")
async def eval(text: str):
    response = await validation.main_debug(text) 
    return JSONResponse(content=response)

@app.get("/backend/v1/eval_fast")
async def eval(text: str):
    response = await validation.main_fast(text) 
    return JSONResponse(content=response)

# Retrieval-Augmented Generation - RAG
@app.get("/backend/rag/dummy")
async def dummy():
    response = [{"claim": "Dummy claim", "label" : "REFUTES", "supports" : 0.1457, "refutes" : 0.8543, "nei": 0.004, "evidence" : "Lorem ipsum dolor sit amet consectetur adipisicing elit. Totam quibusdam architecto velit ut distinctio culpa possimus, debitis corporis, at officiis voluptas ea modi magni omnis saepe earum! Ullam, velit recusandae. Ipsa quibusdam delectus, debitis quam quisquam quasi consectetur ab obcaecati incidunt amet labore, earum velit modi fuga ducimus dignissimos perspiciatis!", "justify" : "Lorem ipsum dolor sit amet consectetur adipisicing elit. Totam quibusdam architecto velit ut distinctio culpa possimus, debitis corporis, at officiis voluptas ea modi magni omnis saepe earum! Ullam, velit recusandae. Ipsa quibusdam delectus, debitis quam quisquam quasi consectetur ab obcaecati incidunt amet labore, earum velit modi fuga ducimus dignissimos perspiciatis!"}]
    return JSONResponse(content=response)

@app.get("/backend/rag/eval")
async def eval(text: str):
    response = await rag.main(text)
    return JSONResponse(content=response)

if __name__ == "__main__":
    uvicorn.run(app, port=8002)