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
    response = [{"claim": "Dummy claim", "label" : 1, "supports" : 0.1457, "refutes" : 0.8543, "evidence" : "Dummy evidence"}]
    return JSONResponse(content=response)

@app.get("/backend/eval")
async def eval(text: str):
    response = await validation.main(text) 
    return JSONResponse(content=response)