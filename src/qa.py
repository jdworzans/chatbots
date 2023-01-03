from typing import Any, Dict, List

import pandas as pd
import requests
import time

from src.reader import READERS
import spacy


# stop_q = {'powieść', '\n', 'utwór', 'mieć', 'państwo', 'co', 'i', 'żyć', 'brzmieć', 'jaki', 'ile', 'zostać', '.', 'Jaką', 'jeden', 'nazywać', 'rzeka', 'oznaczać', 'sam', 'nie', 'miasto', 'światowy', 'stolica', 'morze', 'wyspa', 'święty', 'imię', 'prosić', 'znajdować', 'rok', 'leżeć', 'Który', 'być', 'prezydent', 'liczyć', 'występować', 'się', 'przed', ':', 'dzień', 'autor', 'liczba', 'ten', 'europejski', '”', '?', 'duży', 'góra', 'kraj', 'Polska', 'USA', 'wojna', 'wiek', 'francuski', 'człowiek', 'kontynent', 'pierwszy', 'który', 'czy', 'nazwa', 'to', 'pan', 'bohater', 'za', ',', 'II', 'Jan', 'o', 'język', 'móc', 'dwa', 'pod', 'on', 'zespół', 'wiersz', 'rola', 'należeć', 'według', 'grecki', 'na', 'Jaki', 'postać', 'słowo', 'akcja', '-', '„', 'jak', 'grać', 'dla', 'zajmować', 'gdzie', 'kto', 'raz', '–', 'główny', 'kolor', 'od', 'do', 'zagrać', 'nosić', 'piosenka', 'film', 'przez', 'w', 'a', 'zwierzę', 'tytuł', 'po', 'książka', 'część', 'z', 'pochodzić', 'powstać', 'podczas', 'polski', 'trzy', 'miejsce', 'odbyć', 'nad'}
stop_q = {}

class Answerer:
    def __init__(self, solr_url: str):
        self.solr_url: str = solr_url
        self.extra: Dict = {}
        self.pl = spacy.load("pl_core_news_sm")

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
        doc = self.pl(query)
        tokens = [t for t in doc if len(t) > 1 and t.lemma_ not in stop_q]
        solr_query = " OR ".join([f"content_txt_pl:{str(t)}" for t in tokens])
        ner_spans = doc.ents
        if ner_spans:
            solr_query += " OR " + " OR ".join([f"title_txt_pl:{str(s)}" for s in ner_spans])

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
            return "Nie udało się połączyć z solr"
        if not docs:
            return ""
        for d in docs[:1]:
            result = READERS["PL"].answer(question, [d["content_txt_pl"]])
            if result["answer"]:
                return result["answer"]
        return docs[0]["title_txt_pl"]

if __name__ == "__main__":
    from tqdm import tqdm
    answerer = Answerer("http://solr:8983/solr/dialogs/query")
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data", type=Path)

    args = parser.parse_args()
    out_path = args.data.with_suffix(".out")

    with args.data.open("rt") as in_f:
        for line in tqdm(in_f.readlines()):
            q = line.split("\t")[0]
            a = answerer.answer(q)
            with out_path.open("at") as out_f:
                out_f.write(q + "\t" + a + "\n")
