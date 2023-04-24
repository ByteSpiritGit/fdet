from retriever import TextRetrieverV2
import transformers
import torch
from torch import device, cuda
import nltk
import openai
import os
from dotenv import load_dotenv

class RAG:
    def __init__(self):
        load_dotenv()
        self.retriever = TextRetrieverV2()
        self.device = device("cuda" if cuda.is_available() else "cpu")
        self.num_tokenizer = transformers.RobertaTokenizerFast.from_pretrained("Dzeniks/justification-analyst")
        self.num_model = transformers.RobertaForSequenceClassification.from_pretrained("Dzeniks/justification-analyst")
        self.num_model.to(self.device)
        nltk.download('punkt')
        openai.api_key = os.getenv('openAI_API_KEY')

    async def main(self, text:str) -> list:
        # Document retrieval
        results = []
        claims = nltk.sent_tokenize(text)
        await self.retriever.create_database_DPR(claims)
        for claim in claims:
            evidence, text = self.retriever.extract_passage_str_DPR(claim, 3)
            if evidence == "":
                results.append({"claim": claim, "label" : "NOT ENOUGH INFO", "supports" : None, "refutes" : None, "evidence" : None})
            elif evidence != "":
                justify = await self.generate(claim, evidence)
                label, percent = await self.numerical_evaluation(justify)
                results.append({"claim": claim, "label" : label, "supports" : percent[0], "refutes" : percent[1], "nei": percent[2], "evidence" : evidence, "justify" : justify})
        self.retriever.delete_database()
        return results
    
    async def numerical_evaluation(self, justify) -> tuple:
        tokens = self.num_tokenizer(justify ,return_tensors="pt")
        tokens = tokens.to(self.device)
        with torch.no_grad():
            self.num_model.eval()
            logits = self.num_model(**tokens)
        label = torch.argmax(logits[0], dim=1).item()
        per = torch.nn.functional.softmax(logits[0], dim=1).tolist()[0]
        label_map = {0: "SUPPORTS", 1: "REFUTES", 2: "NOT ENOUGH INFO"}
        return label, per

    async def generate(self, claim, evidence) -> str:
        prompt_template = f"claim: {claim} evidence: {evidence}"
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=100,
        messages=[
                {"role": "system", "content": "You are a fact checking specialist. Justify if the claim is supports, not enough info, refutes. Use your knowledge and evidence."},
                {"role": "user", "content": prompt_template},
            ]
        )
        justify = response["choices"][0]["message"]["content"]
        return justify