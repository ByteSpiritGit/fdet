# Fact-Checking System Backend

Welcome to the backend of the Fact-Checking System. This system provides various endpoints that can be used to evaluate the accuracy of text.

## Endpoints

Please use the following endpoints to access the system:

- `/backend/v1/dummy`: A dummy endpoint for testing purposes.
- `/backend/v1/eval?text=...`: This endpoint evaluates the accuracy of the provided text.
- `/backend/v1/eval_debug?text=...`: This endpoint provides detailed debugging information about the evaluation process.
- `/backend/v1/eval_fast?text=...`: This endpoint provides a faster evaluation process, but may sacrifice some accuracy.
- `/backend/rag/dummy`: A dummy endpoint for the Retrieval-Augmented Generation (RAG) model for testing purposes.
- `/backend/rag/eval?text=...`: This endpoint uses the RAG model to evaluate the accuracy of the provided text.
- `/backend/rag/eval_DPR?text=...`: This endpoint uses the RAG model with Dense Passage Retrieval (DPR) to evaluate the accuracy of the provided text.
- `/backend/rag/eval_Ada?text=...`: This endpoint uses the RAG model with Adaptive Retrieval (Ada) to evaluate the accuracy of the provided text.
- `/backend/rag/eval_BM25?text=...`: This endpoint uses the RAG model with BM25 retrieval to evaluate the accuracy of the provided text.

## Usage

To use the Fact-Checking System Backend, simply make a request to the desired endpoint with the required parameters. For endpoints that require the text parameter, replace `...` with the text you want to evaluate.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
