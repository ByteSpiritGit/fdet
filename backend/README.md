# API Endpoints

## Classification with Advanced Search

### `/backend/v1/dummy`

Returns a dummy classification result.

### `/backend/v1/eval`

Evaluates a given text and returns a classification result.

### `/backend/v1/eval_fast`

Evaluates a given text and returns a classification result (faster version).

## Retrieval-Augmented Generation - RAG

### `/backend/rag/dummy`

Returns a dummy RAG result.

### `/backend/rag/eval_dpr`

Evaluates a given text and returns a RAG result using DPR instances.

### `/backend/rag/eval_ada`

Evaluates a given text and returns a RAG result using ADA instances.

### `/backend/rag/eval_bm25`

Evaluates a given text and returns a RAG result using BM25 instances.

## Miscellaneous

### `/coffee`

Returns an HTTP 418 response with the message "I'm a teapot".
