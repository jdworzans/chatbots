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
            cache_dir="cache"
        )

    def answer(self, query: str, context: str) -> dict:
        """
        Returns answer to a question given context and query.
        """
        return self.model({'question': query, 'context': context})


READERS = {
    "EN": Reader("deepset/roberta-base-squad2"),
    "PL": Reader("henryk/bert-base-multilingual-cased-finetuned-polish-squad2"),
}
