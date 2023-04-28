import nltk
from anlys import remove_stop_words
import logging
from torch import no_grad, argmax, softmax, device, cuda
from transformers import RobertaTokenizerFast, RobertaForSequenceClassification

class Main():
    def __init__(self) -> None:
        self.device = device("cuda" if cuda.is_available() else "cpu")
        logging.info(f"Using device: {self.device}")
        self.tokenizer = RobertaTokenizerFast.from_pretrained('Dzeniks/roberta-fact-check', longest_first=True)
        self.model = RobertaForSequenceClassification.from_pretrained('Dzeniks/roberta-fact-check', return_dict=True, num_labels=2)
        self.nei = RobertaForSequenceClassification.from_pretrained('Dzeniks/roberta-nei-fact-check', return_dict=True, num_labels=2)
        self.device = device("cuda" if cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.nei.to(self.device)

    def main(self, text, retriever):
        # Document retrieval
        results = []
        claims = nltk.sent_tokenize(text)
        retriever.create_database(text)
        retriever.update_embed()
        for claim in claims:
            evidence, text, url = retriever.retrieve(claim, 3)
            if evidence == "":
                results.append({"claim": claim, "label" : "NOT ENOUGH INFO", "supports" : None, "refutes" : None,"nei": None,"ei":None, "evidence" : None})
            elif evidence != "":
                tokens = self.tokenizer.encode_plus(remove_stop_words(claim.lower()), evidence, truncation="longest_first" , max_length=512, padding="max_length", return_tensors="pt")                                     
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
                    out = "SUPPORTS"
                    if argmax(prediction.logits) == 1: out = "REFUTES"
                    softMax = softmax(prediction.logits, dim=1)
                    supports, refutes = float(softMax[0][0]), float(softMax[0][1]) 
                    results.append({"claim": claim, "label" : out, "supports" : supports, "refutes" : refutes, 'ei': ei, "nei": nei, "evidence" : evidence, "url": url})
                else:
                    results.append({"claim": claim, "label" : "NOT ENOUGH INFO", "supports" : None, "refutes" : None, 'ei': ei, "nei": nei, "evidence" : text, "url": url})
        retriever.delete_database()
        return results


    def main_debug(self, text, retriever):
        # Document retrieval
        results = []
        nltk.download('punkt')
        claims = nltk.sent_tokenize(text)
        retriever.create_database(claims)
        retriever.update_embed()
        for claim in claims:
            evidence, text, url = retriever.retrieve(claim, 3)
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
        retriever.delete_documents()
        return results