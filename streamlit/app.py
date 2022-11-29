import pandas as pd
import requests
from reader import readers

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

    r = requests.get(
        SOLR_URL,
        json={"query": solr_query, "params": {"debugQuery": True}}
    )

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
    q_type = st.radio(label="Type", options=["Chat", "Question"])
    question = st.text_input("Enter question")
    more_info = st.checkbox("Show details")

    if q_type == "Chat":
        answer, info = query_solr(question, language.lower())
        st.write(answer)
        if more_info:
            st.caption("Solr")
            docs = pd.DataFrame(info["response"].get("response", {}).get("docs", [])).drop(
                columns=["id", "_version_"], errors="ignore",
            )
            st.dataframe(docs, use_container_width=True)

    elif q_type == "Question":
        context, info = query_solr(question, language.lower())
        result = readers[language].answer(question, context)

        st.write(result['answer'])

        if more_info:
            st.caption("Solr")
            docs = pd.DataFrame(info["response"].get("response", {}).get("docs", [])).drop(
                columns=["id", "_version_"], errors="ignore",
            )
            st.dataframe(docs, use_container_width=True)

            st.caption("Reader")
            st.write(result)
