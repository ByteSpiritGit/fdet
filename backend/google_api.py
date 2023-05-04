import requests
import nltk
import asyncio
import os
from dotenv import load_dotenv

class googleAPI:

    def __init__(self):
        load_dotenv()
        self.API = os.getenv("google_API_KEY")  
        self.search_endpoint = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

    def main(self, text):
        # Document retrieval
        results = []
        claims = nltk.sent_tokenize(text)
        for i in claims:
            result = self.google_api(i)
            if result is not None:
                results += result
        return results

    def google_api(self, text):
        response = requests.get(self.search_endpoint, params={"key": self.API,"query": text, "languageCode": "en-US"})
        if response.status_code == 200:
            response = response.json()
            response_out = []
            if response == {}:
                return
            for i in response["claims"]:
                claim = i["text"]
                url = i["claimReview"][0]["url"]
                evidence_list = [i["claimReview"][0].get("textualRating") ,i["claimReview"][0].get("claimReview") ,i["claimReview"][0].get("title")]
                evidence = " - ".join(([elem for elem in evidence_list if elem is not None]))
                # evidence = f"{evidence} - {label}."
                response_out.append(((claim, evidence, url)))
            return response_out
        else:            
            print(f"Error with API request: {response.status_code}")
        return None

