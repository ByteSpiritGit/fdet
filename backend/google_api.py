import requests
import nltk
import os
from dotenv import load_dotenv

class googleAPI:

    def __init__(self):
        load_dotenv()
        self.API = os.getenv("google_API_KEY")  
        self.search_endpoint = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

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

