import nltk
import requests
import anlys
from torch import no_grad, argmax, softmax, device, cuda
from transformers import RobertaTokenizerFast, RobertaForSequenceClassification, logging
from retriever import TextRetrieverV2
logging.set_verbosity_error()
class TextValidate():
    def __init__(self) -> None:
        print(f"Loading text validator")
        nltk.download('punkt')

        self.device = device("cuda" if cuda.is_available() else "cpu")
        print(f"You are using {self.device}")

        self.tokenizer = RobertaTokenizerFast.from_pretrained('Dzeniks/roberta-fact-check', longest_first=True)
        self.model = RobertaForSequenceClassification.from_pretrained('Dzeniks/roberta-fact-check', return_dict=True, num_labels=2)
        self.model.to(self.device)

        self.nei = RobertaForSequenceClassification.from_pretrained('Dzeniks/roberta-nei-fact-check', return_dict=True, num_labels=2)
        self.nei.to(self.device)
        self.retriever = TextRetrieverV2()

        self.API = "AIzaSyDUeOlRcaTFeUNzEw8QTDb7G6zv4QXgaMs"
        self.search_endpoint = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
        print(f"Loaded")

    async def main(self, text):
        # Document retrieval
        results = []
        claims = nltk.sent_tokenize(text)
        await self.retriever.create_database_DPR(claims)
        for claim in claims:
            evidence, text = self.retriever.extract_passage_str_DPR(claim, 1)
            if evidence == "":
                print("NOT ENOUGH INFO")
                results.append({"claim": claim, "label" : "NOT ENOUGH INFO", "supports" : None, "refutes" : None, "evidence" : None})
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
                    results.append({"claim": claim, "label" : out, "supports" : supports, "refutes" : refutes, 'ei': ei, "nei": nei, "evidence" : evidence})
                else:
                    print("NOT ENOUGH INFO")
                    results.append({"claim": claim, "label" : "NOT ENOUGH INFO", "supports" : ei, "refutes" : nei, "evidence" : text})
        self.retriever.delete_database()
        print(results)
        return results

    async def main_fast(self, text):
        # Document retrieval
        results = []
        claims = nltk.sent_tokenize(text)
        await self.retriever.create_database_BM25(claims)
        for claim in claims:
            evidence = self.retriever.extract_passage_str_BM25(claim, 1)
            if evidence == "":
                print("NOT ENOUGH INFO")
                results.append({"claim": claim, "label" : "NOT ENOUGH INFO", "supports" : None, "refutes" : None, 'ei': None, "nei": None, "evidence" : None})
            elif evidence != "":
                tokens = self.tokenizer.encode_plus(claim, evidence, truncation="longest_first" , max_length=512, padding="max_length", return_tensors="pt")                                     
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
                    results.append({"claim": claim, "label" : out, "supports" : supports, "refutes" : refutes, 'ei': ei, "nei": nei, "evidence" : evidence})
                else:
                    print("NOT ENOUGH INFO")
                    results.append({"claim": claim, "label" : "NOT ENOUGH INFO", "supports" : None, "refutes" : None, 'ei': ei, "nei": nei, "evidence" : evidence})

        self.retriever.delete_database()
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
            evidence = self.retriever.extract_passage(claim, 3)
            if evidence == "":
                results.append({"claim": claim, "label" : "NOT ENOUGH INFO", "supports" : None, "refutes" : None, "evidence" : None})
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
                results.append({"claim": claim, "label" : out, "supports" : supports, "refutes" : refutes, 'ei': ei, "nei": nei, "evidence" : evidence})

        self.retriever.delete_database()
        print(results)
        return results

    async def main_google(self, text):
        # Document retrieval
        results = []
        claims = nltk.sent_tokenize(text)
        for i in claims:
            results.append(await self.google_api(i))
        return results

    async def google_api(self, text):
        response = requests.get(self.search_endpoint, params={"key": self.API,"query": text, "languageCode": "en-US"})
        if response.status_code == 200:
            response = response.json()
            label = response["claims"][0]["claimReview"][0]["textualRating"]
            evidence = response["claims"][0]["claimReview"][0]["claimReviewed"]
            return {"claim": text, "label": label, "supports" : None, "refutes" : None, "evidence" : evidence}
        else:            
            print(f"Error with API request: {response.status_code}")
        return None

