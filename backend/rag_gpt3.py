import asyncio
import os
from typing import Any

import nltk
import openai
import torch
import transformers
from dotenv import load_dotenv
from torch import device, cuda

from rag import RAG


class GPT3(RAG):
    def __init__(self) -> None:
        super().__init__()
        load_dotenv()
        self.device = device("cuda" if cuda.is_available() else "cpu")
        self.num_tokenizer = transformers.RobertaTokenizerFast.from_pretrained("Dzeniks/justification-analyst")
        self.num_model = transformers.RobertaForSequenceClassification.from_pretrained("Dzeniks/justification-analyst")
        self.num_model.to(self.device)
        openai.api_key = os.getenv('openAI_API_KEY')

    def main(self, text, retriever):
        return asyncio.run(self.async_main(text, retriever))

    async def async_main(self, text: str, retriever):
        claims = nltk.sent_tokenize(text)

        async def process_claim(claim, retriever) -> dict[str, str | None | Any] | dict[str, str | Any]:
            try:
                evidence, text, url = retriever.retrieve_RAG(claim)
            except Exception as e:
                return {"claim": claim, "label": "NOT ENOUGH INFO", "supports": None, "refutes": None, "evidence": None}
            justify = await self.generate(claim, evidence)
            label, percent = await self.numerical_evaluation(justify)
            return {"claim": claim, "label": label, "supports": percent[0], "refutes": percent[1], "nei": percent[2],
                    "evidence": text, "justify": justify, "url": url}

        tasks = [process_claim(claim, retriever) for claim in claims]
        results = await asyncio.gather(*tasks)
        return results

    async def numerical_evaluation(self, justify) -> tuple:
        tokens = self.num_tokenizer(justify, return_tensors="pt")
        tokens = tokens.to(self.device)
        with torch.no_grad():
            self.num_model.eval()
            logits = self.num_model(**tokens)
        label = torch.argmax(logits[0], dim=1).item()
        per = torch.nn.functional.softmax(logits[0], dim=1).tolist()[0]
        label_map = {0: "SUPPORTS", 1: "REFUTES", 2: "NOT ENOUGH INFO"}
        return label_map[label], per

    async def generate(self, claim, evidence) -> str:
        prompt_template = f"claim: {claim} evidence: {evidence}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens=75,
            frequency_penalty=0.5,
            messages=[
                {"role": "system",
                 "content": "Classify if the claim is supports, not enough info or refutes and justify. Use evidence and knowledge base."},
                {"role": "user", "content": prompt_template},
            ]
        )
        justify = response["choices"][0]["message"]["content"]
        return justify
