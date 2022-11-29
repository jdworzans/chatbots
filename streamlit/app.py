import pandas as pd
import requests
from typing import List, Dict, Tuple
from reader import readers

import streamlit as st

SOLR_URL = "http://solr:8983/solr/dialogs/query"


def query_solr(query: str, language: str) -> Tuple[str, Dict]:
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

def query_wiki(query: str) -> Tuple[List, str]:
    """
    Function to query the Solr database for wiki articles.

    Parameters
    ----------
        query, str:
            The question to be searched
    """
    if query is None:
        return [], ""

    solr_query = f"content_txt_pl: {query} OR "
    solr_query += " OR ".join([f"content_txt_pl:{t}" for t in query.split()])

    r = requests.get(
        SOLR_URL,
        json={"query": solr_query, "params": {"debugQuery": True}}
    )

    if not r.ok:
        return [], r.text
    response = r.json()
    docs = response["response"]["docs"]
    if not docs:
        return [], response
    info = {
        "solr_query": solr_query,
        "response": response,
    }
    return docs, info

if __name__ == "__main__":
    st.title("Sparse Retrieval QA")

    q_type = st.radio(label="Type", options=["Chat", "Question"])
    question = st.text_input("Enter question")
    more_info = st.checkbox("Show details")

    if q_type == "Chat":
        language = st.radio(label="Language", options=["PL", "EN"])
        answer, info = query_solr(question, language.lower())
        st.write(answer)
        if more_info:
            st.caption("Solr")
            docs = pd.DataFrame(info["response"].get("response", {}).get("docs", [])).drop(
                columns=["id", "_version_"], errors="ignore",
            )
            st.dataframe(docs, use_container_width=True)

    elif q_type == "Question":
        docs, info = query_wiki(question)
        if docs:
            if len(docs) >= 10:
                contexts = [docs[i]["content_txt_pl"] for i in range(10)]
            elif len(docs) < 10:
                contexts = [docs[i]["content_txt_pl"] for i in range(len(docs))]
            results = [readers["PL"].answer(question, context) for context in contexts]
            scores = [result['score'] for result in results]
            idx_max = scores.index(max(scores))
            result = results[idx_max]
            st.write(result['answer'])
            if more_info:
                st.caption("Solr")
                docs = pd.DataFrame(info["response"].get("response", {}).get("docs", [])).drop(
                    columns=["id", "_version_"], errors="ignore",
                )
                st.dataframe(docs, use_container_width=True)

                st.caption("Reader")
                #st.write(info["response"]["debug"]["explain"])
                #st.write(info)
                st.write(results)
