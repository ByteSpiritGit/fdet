import nltk
import anlys
from BM25 import retriever_BM25
from DPR import retriever_DPR
from Ada import retriever_Ada
from torch import no_grad, argmax, softmax, device, cuda
from transformers import RobertaTokenizerFast, RobertaForSequenceClassification

class Main():
    def __init__(self, retriever="BM25") -> None:
        self.device = device("cuda" if cuda.is_available() else "cpu")
        print(f"You are using {self.device}")
        self.tokenizer = RobertaTokenizerFast.from_pretrained('Dzeniks/roberta-fact-check', longest_first=True)
        self.model = RobertaForSequenceClassification.from_pretrained('Dzeniks/roberta-fact-check', return_dict=True, num_labels=2)
        self.nei = RobertaForSequenceClassification.from_pretrained('Dzeniks/roberta-nei-fact-check', return_dict=True, num_labels=2)
        self.device = device("cuda" if cuda.is_available() else "cpu")
        # logger.info(f"You are using {self.device}")
        self.model.to(self.device)
        self.nei.to(self.device)

    async def main(self, text):
        # Document retrieval
        results = []
        claims = nltk.sent_tokenize(text)
        await self.retriever.create_database(claims)
        for claim in claims:
            evidence, text, url = self.retriever.extract_passage_str_DPR(claim, 1)
            if evidence == "":
                print("NOT ENOUGH INFO")
                results.append({"claim": claim, "label" : "NOT ENOUGH INFO", "supports" : None, "refutes" : None,"nei": None,"ei":None, "evidence" : None})
            elif evidence != "":
                tokens = self.tokenizer.encode_plus(anlys.remove_stop_words(claim.lower()), evidence, truncation="longest_first" , max_length=512, padding="max_length", return_tensors="pt")                                     
                # NEI Classification
                self.nei.eval()
                with no_grad(): 
                    tokens = tokens.to(self.device)                    
                    prediction = self.nei(**tokens)
                out = "SUPPORTS"
                if argmax(prediction.logits) == 1: out = "REFUTES"
                softMax = softmax(prediction.logits, dim=1)
                ei, nei = float(softMax[0][0]), float(softMax[0][1]) 
                # SUP,REF Classification
                if argmax(prediction.logits) == 0:
                    self.model.eval()
                    with no_grad(): 
                        tokens = tokens.to(self.device)                    
                        prediction = self.model(**tokens)
                    print(claim)
                    out = "SUPPORTS"
                    if argmax(prediction.logits) == 1: out = "REFUTES"
                    softMax = softmax(prediction.logits, dim=1)
                    supports, refutes = float(softMax[0][0]), float(softMax[0][1]) 
                    print(f"Claim is {out}\nSupports {100*supports:>0.1f} %, \tRefutes {100*refutes:>0.1f} %")
                    print(f"Evidence:\n{evidence}")
                    results.append({"claim": claim, "label" : out, "supports" : supports, "refutes" : refutes, 'ei': ei, "nei": nei, "evidence" : evidence, "url": url})
                else:
                    print("NOT ENOUGH INFO")
                    results.append({"claim": claim, "label" : "NOT ENOUGH INFO", "supports" : None, "refutes" : None, 'ei': ei, "nei": nei, "evidence" : text})
        self.retriever.delete_documents()
        print(results)
        return results


    async def main_debug(self, text):
        # Document retrieval
        results = []
        nltk.download('punkt')
        claims = nltk.sent_tokenize(text)
        claims = [item for item in claims if item != ""]
        await self.retriever.create_database(claims)
        for claim in claims:
            evidence, text, url = self.retriever.extract_passage(claim, 3)
            if evidence == "":
                results.append({"claim": claim, "label" : "NOT ENOUGH INFO", "supports" : None, "refutes" : None,"nei": None, 'ei': None, "evidence" : None})
            elif evidence != "":
                tokens = self.tokenizer.encode_plus(claim, evidence, truncation="longest_first" , max_length=512, padding="max_length", return_tensors="pt")                                     
                # NEI Classification
                self.nei.eval()
                with no_grad(): 
                    tokens = tokens.to(self.device)                    
                    prediction = self.nei(**tokens)
                softMax = softmax(prediction.logits, dim=1)
                ei, nei = float(softMax[0][0]), float(softMax[0][1]) 
                # SUP,REF Classification
                self.model.eval()
                with no_grad(): 
                    tokens = tokens.to(self.device)                    
                    prediction = self.model(**tokens)
                out = "SUPPORTS"
                if argmax(prediction.logits) == 1: out = "REFUTES"
                softMax = softmax(prediction.logits, dim=1)
                supports, refutes = float(softMax[0][0]), float(softMax[0][1]) 
                results.append({"claim": claim, "label" : out, "supports" : supports, "refutes" : refutes, 'ei': ei, "nei": nei, "evidence" : text, "url": url})

        self.retriever.delete_documents()
        print(results)
        return results