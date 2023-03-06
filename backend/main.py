from torch import no_grad, argmax, softmax, device, cuda
from transformers import AlbertTokenizerFast, AlbertForSequenceClassification, logging
from retriever import TextRetrieverV2
logging.set_verbosity_error()

class TextValidate():

    def __init__(self) -> None:
        print(f"Loading text validator")
        self.device = device("cuda" if cuda.is_available() else "cpu")
        print(f"You are using {self.device}")
        self.tokenizer = AlbertTokenizerFast.from_pretrained('Dzeniks/alberta_fact_checking', longest_first=False)
        self.model = AlbertForSequenceClassification.from_pretrained('Dzeniks/alberta_fact_checking', return_dict=True, num_labels=2)    
        self.model.to(self.device)
        self.retriever = TextRetrieverV2()
        print(f"Loaded")

    def main(self, text):
        # Document retrieval
        results = []
        claims = text.split(".")
        claims = [item for item in claims if item != ""]
        self.retriever.create_database(claims)
        for claim in claims:
            evidence = self.retriever.extract_passage(claim, 3)
            if evidence == "":
                print("NOT ENOUGH INFO")
                results.append({"claim": claim, "label" : "NOT ENOUGH INFO", "supports" : None, "refutes" : None, "evidence" : None})
            elif evidence != "":
                tokens = self.tokenizer.encode_plus(claim, evidence, truncation="longest_first" , max_length=512, padding="max_length", return_tensors="pt")                                     
                # Classification
                self.model.eval()
                with no_grad(): 
                    tokens = tokens.to(self.device)
                    inputIDs = tokens["input_ids"].squeeze(1)
                    attention = tokens["attention_mask"].squeeze(1)
                    typeIds = tokens["token_type_ids"].squeeze(1)
                    prediction = self.model(input_ids=inputIDs, attention_mask=attention, token_type_ids=typeIds)
                print(claim)
                out = "SUPPORTS"
                if argmax(prediction.logits) == 1: out = "REFUTES"
                softMax = softmax(prediction.logits, dim=1)
                supports, refutes = float(softMax[0][0]), float(softMax[0][1]) 
                print(f"Claim is {out}\nSupports {100*supports:>0.1f} %, \tRefutes {100*refutes:>0.1f} %")
                print(f"Evidence:\n{evidence}")
                results.append({"claim": claim, "label" : out, "supports" : supports, "refutes" : refutes, "evidence" : evidence})
        self.retriever.delete_database()
        return results
