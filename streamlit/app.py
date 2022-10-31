import json
from urllib.request import urlopen
from urllib.parse import quote_plus

import streamlit as st

SOLR_URL = "http://localhost:8983/solr/#/dialogs/"

def query_solr(query:str) -> str:
    """
    Function to query the Solr database with a question

    Parameters
    ----------
        query, str:
            The question to be searched
    """
    if query is not None:
        query_string = f"Q:\"{query}\""
        query_url = SOLR_URL +"select?q=" +quote_plus(query_string)
        with urlopen(query_url) as connection:
            response = json.load(connection)
            if response['response']['numFound'] == 0:
                return None
            return response['response']['docs'][0]['A']
    return None

if __name__=="__main__":
    st.title("Sparse Retrieval QA")
    question = st.text_input("Enter question")
    if question:
        answer = query_solr(question)
        st.write(answer)
