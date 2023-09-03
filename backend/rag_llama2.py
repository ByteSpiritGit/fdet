import asyncio
from typing import Any

import nltk
import torch
import transformers
from peft import PeftModel
from torch import device, cuda
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

from rag import RAG


class Llama_2(RAG):

    def __init__(self):
        super().__init__()
        self.device = device("cuda" if cuda.is_available() else "cpu")
        self.num_tokenizer = transformers.RobertaTokenizerFast.from_pretrained("Dzeniks/justification-analyst")
        self.num_model = transformers.RobertaForSequenceClassification.from_pretrained("Dzeniks/justification-analyst")
        self.num_model.to(self.device)

        self.adapter_name = "Dzeniks/Llama-2-7b-PEFT-Justification"
        self.model_name = "meta-llama/Llama-2-7b-hf"

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            load_in_4bit=True,
            quantization_config=BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.bfloat16,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type='nf4'
            ),
            device_map="auto"
        )
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, use_auth_token=True)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model = PeftModel.from_pretrained(self.model, self.adapter_name)
        self.model.eval()
        self.instruction = "Classify if the claim is supports, not enough info or refutes and justify." \
                           "Use evidence and knowledge base."


    def get_prompt(self, claim, evidence):
        INTRO_BLURB = "Below is an instruction that describes a task. Write a response that appropriately completes the request."
        INSTRUCTION_KEY = "### Instruction:"
        INPUT_KEY = "Input:"

        blurb = f"{INTRO_BLURB}"
        instruction = f"{INSTRUCTION_KEY}\n{self.instruction}"
        input_context = f"{INPUT_KEY}\nClaim: {claim}\nEvidence: {evidence}"

        parts = [part for part in [blurb, instruction, input_context] if part]

        prompt = "\n\n".join(parts)
        return prompt

    def get_response(self, raw_response: str) -> str:
        substring = "justification:"
        response_part: list = raw_response.split("### Response:")
        if response_part is not None and len(response_part) > 1:
            response: str = response_part[1]
            try:
                split_index = response.lower().find(substring)
                return response[split_index + len(substring) + 1:].strip()
            except IndexError:
                return response

    def main(self, text, retriever):
        return asyncio.run(self.async_main(text, retriever))

    async def async_main(self, text: str, retriever) -> tuple[Any]:
        claims = nltk.sent_tokenize(text)

        async def process_claim(claim, retriever):
            try:
                evidence, text, url = retriever.retrieve_RAG(claim, top_k=6, max_len=300)
            except:
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
        tokenized_prompt = self.tokenizer(self.get_prompt(claim, evidence) + "\n### Response: ", return_tensors="pt", padding=True,
                                     truncation=True, max_length=1024)
        with torch.no_grad():
            outputs = self.model.generate(input_ids=tokenized_prompt["input_ids"].to("cuda"), max_new_tokens=100, early_stopping=True)
            justify = self.tokenizer.batch_decode(outputs.detach().cpu().numpy(), skip_special_tokens=True)[0]
        return self.get_response(justify)
