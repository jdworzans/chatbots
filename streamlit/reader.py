from transformers import pipeline


class Reader:
    """
    Reader class that parses question and context.
    """
    def __init__(
        self,
        en_model_name="deepset/roberta-base-squad2",
        pl_model_name="henryk/bert-base-multilingual-cased-finetuned-polish-squad2"  # noqa
    ):
        self.en_model_name = en_model_name
        self.pl_model_name = pl_model_name
        self.load_model()

    def load_model(self):
        """
        Loads QA models for Polish and English.
        """
        self.en_model = pipeline(
            'question-answering',
            model=self.en_model_name,
            tokenizer=self.en_model_name
        )

        self.pl_model = pipeline(
            'question-answering',
            model=self.pl_model_name,
            tokenizer=self.pl_model_name
        )

    def answer(
        self,
        query: str,
        context: str,
        lang: str = "en"
    ) -> dict:
        """
        Returns answer to a question given context and query.
        """
        model = self.pl_model
        if lang == "en":
            model = self.en_model

        return model(
            {
                'question': query,
                'context': context
            }
        )
