from typing import List, Union

from transformers import pipeline


class Reader:
    """
    Reader class that parses question and context.
    """
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.load_model()

    def load_model(self):
        """
        Loads QA model.
        """
        self.model = pipeline(
            "question-answering",
            model=self.model_name,
            tokenizer=self.model_name,
            cache_dir="cache",
            handle_impossible_answer=True,
        )

    def answer(self, query: str, contexts: Union[str, List[str]]) -> dict:
        """
        Returns answer to a question given context and query.
        """
        if isinstance(contexts, str):
            contexts = [contexts]
        questions = [
            {"question": query, "context": context} for context in contexts
        ]
        return self.model(questions)


READERS = {
    "EN": Reader("deepset/roberta-base-squad2"),
    "PL": Reader("azwierzc/herbert-large-poquad")
}
