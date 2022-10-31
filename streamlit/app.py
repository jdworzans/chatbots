import requests
import streamlit as st


SOLR_URL = "http://solr:8983/solr/dialogs/query"


def query_solr(query: str, language: str) -> str:
    """
    Function to query the Solr database with a question

    Parameters
    ----------
        query, str:
            The question to be searched
        language, str:
            Question language abbreviation
    """
    if query is None:
        return None
    r = requests.get(SOLR_URL, json={"query": f"Q_txt_{language}:{query}"})
    if not r.ok:
        return None
    response = r.json()
    docs = response["response"]["docs"]
    if not docs:
        return None
    return docs[0][f"A_txt_{language}"]


if __name__ == "__main__":
    st.title("Sparse Retrieval QA")
    language = st.radio(label="Language", options=["PL", "EN"])
    question = st.text_input("Enter question")
    if question:
        answer = query_solr(question, language.lower())
        st.write(answer)
