# Backend api function guide

## FAST API start command
```
uvicorn api:app --reload
```
or
```
py api.py 
```

Plain text <br>
    "/backend"

Url for dummy function <br>
    "/backend/dummy"

Url for evaluation <br>
    "/backend/eval"

Url for text input <br>
    "/backend/eval_debug"


Url for text input <br>
    "/backend/eval_fast"
    

When you call the function, append a parameter named text with text to check. <br>
Example file in backend/test.py
