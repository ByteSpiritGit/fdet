import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from main import TextValidate

app = FastAPI()
validation = TextValidate()

# example = "Andrej Babiš said he would not help baltic states and Poland if they were invaded"

@app.get("/backend")
async def root():
    return "backend"

@app.get("/backend/dummy")
async def dummy():
    response = [{"claim": "Dummy claim", "label" : "REFUTES", "supports" : 0.1457, "refutes" : 0.8543, "evidence" : "Lorem ipsum dolor sit amet consectetur adipisicing elit. Totam quibusdam architecto velit ut distinctio culpa possimus, debitis corporis, at officiis voluptas ea modi magni omnis saepe earum! Ullam, velit recusandae. Ipsa quibusdam delectus, debitis quam quisquam quasi consectetur ab obcaecati incidunt amet labore, earum velit modi fuga ducimus dignissimos perspiciatis!"}]
    return JSONResponse(content=response)

@app.get("/backend/eval")
async def eval(text: str):
    response = await validation.main(text) 
    return JSONResponse(content=response)

@app.get("/backend/eval_debug")
async def eval(text: str):
    response = await validation.main_debug(text) 
    return JSONResponse(content=response)


if __name__ == "__main__":
    uvicorn.run(app, port=8002)