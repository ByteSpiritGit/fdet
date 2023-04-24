# Backend api function guide

## FAST API start command
```
uvicorn api:app --reload
```
or
```
py api.py 
```

Plain text with help GET<br>
    "/backend"

Url for v1 dummy function GET<br>
    "/backend/v1/dummy"

Url for v1 evaluation GET<br>
    "/backend/v1/eval"

Url for v1 text input GET<br>
    "/backend/v1/eval_debug"

Url for v1 text input GET<br>
    "/backend/v1/eval_fast"

Url for RAG dummy function GET<br>
    "/backend/rag/dummy"

Url for RAG text input GET<br>
    "/backend/rag/eval"


When you call the endpoint, append a parameter named text with text to check. <br>
Example file in backend/test.py