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
        return None, None
    solr_query = f"Q_txt_{language}: {query} OR "
    solr_query += " OR ".join([f"Q_txt_{language}:{t}" for t in query.split()])
    r = requests.get(SOLR_URL, json={"query": solr_query, "params": {"debugQuery": True}})
    if not r.ok:
        return None, r.text
    response = r.json()
    docs = response["response"]["docs"]
    if not docs:
        return None, response
    info = {
        "solr_query": solr_query,
        "response": response,
    }
    return docs[0][f"A_txt_{language}"], info


if __name__ == "__main__":
    st.title("Sparse Retrieval QA")
    language = st.radio(label="Language", options=["PL", "EN"])
    question = st.text_input("Enter question")
    if question:
        answer, info = query_solr(question, language.lower())
        st.write(answer)
        more_info = st.checkbox("Show details")
        if more_info:
            st.write(info)
