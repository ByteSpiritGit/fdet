# Starting the server
```py
python manage.py runserver
```
## **Superusers:** <br>
1. Fdet


## **URLS:** 
admin - `/admin` <br>
### PAGES
Homepage - `/` <br>
EvalOutput - `/eval_output` <br>
RegisterPage - `/registerPage` <br>
LoginPage - `/loginPage` <br>
CSRF - `/csrf_view` <br>

### USERS EXT
Registration - `/registration` <br>
Login - `/login` <br>
Logout - `/logout` <br>
Authentication - `/authentication` <br>

### EVALUATIONS

V1 Dummy backend - `/v1/dummy_backend` <br>
V1 Evaluation - `/v1/eval` <br>
V1 Evaluation fast - `/v1/eval_fast` <br>

Rag Dummy Backend - `rag/dummy_backend` <br>
Rag Evaluation - `/rag/eval` <br>
Rag Evaluation DPR - `/rag/eval_DPR` <br>
Rag Evaluation Ada - `/rag/eval_ada` <br>
Rag Evaluation BM25 - `/rag/eval_bm25` <br>


### FEEDBACKS
Eval feedback - `/eval_feedback` <br>
User feedback - `/user_feedback` <br>

## **Notes!** <br>
If public: Debug = False

**If changing models.py always run makemigrations & migrate**
