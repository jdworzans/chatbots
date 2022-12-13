from typing import Any, Dict, List

import pandas as pd
import requests
import time

from src.reader import READERS


class Answerer:
    def __init__(self, solr_url: str):
        self.solr_url: str = solr_url
        self.extra: Dict = {}

    def query_wiki(self, query: str) -> List[Dict[str, Any]]:
        """
        Function to query the Solr database for wiki articles.

        Parameters
        ----------
            query, str:
                The question to be searched
        """
        if not query:
            return []
        solr_query = f"content_txt_pl: {query} OR "
        solr_query += " OR ".join([f"content_txt_pl:{t}" for t in query.split()])

        request_json = {"query": solr_query, "params": {"debugQuery": True}}
        r = requests.get(self.solr_url, json=request_json)
        r.raise_for_status()
        response = r.json()
        self.extra["solr"] = response
        return response["response"]["docs"]

    def answer(self, question: str):
        try:
            docs =  self.query_wiki(question)
        except requests.exceptions.HTTPError as err:
            time.sleep(1)
            try:
                docs =  self.query_wiki(question)
            except requests.exceptions.HTTPError as err:
                return "Nie udało się połączyć z solr"
        if not docs:
            return ""
        results = READERS["PL"].answer(question, [d["content_txt_pl"] for d in docs])
        best = max(results, key=lambda result: result["score"])

        self.extra["readers"] = pd.DataFrame(docs).join(pd.DataFrame(results))
        return best["answer"]

if __name__ == "__main__":
    from tqdm import tqdm
    answerer = Answerer("http://solr:8983/solr/dialogs/query")

    with open("data/questions.tsv", "rt") as in_f:
        for line in tqdm(in_f.readlines()):
            q = line.split("\t")[0]
            a = answerer.answer(q)
            with open("data/found_answers.txt", "at") as out_f:
                out_f.write(q + "\t" + a + "\n")
