# Starting the server
```py
python manage.py runserver
```
## **Superusers:** <br>
1. Fdet


## **URLS:** 
admin - "/admin" <br>
### PAGES
Homepage - "" <br>
OldEvaluation - "/old_eval" <br>
EvalOutput - "/eval_output" <br>

### EVALUATIONS
CSRF - "/csrf_view" <br>

Evaluation - "/evaluation" <br>
Evaluation fast - "/evaluation_fast" <br>
Dummy - "/dummy" <br>
Dummy backend - "/dummy_backend" <br>

Rag Evaluation - "/rag_evaluation" <br>
Rag dummy backend - "/rag_dummy_backend" <br>


### FEEDBACKS
Eval feedback - "/eval_feedback" <br>

## **Notes!** <br>
If public: Debug = False

**If changing models.py always run makemigrations & migrate**