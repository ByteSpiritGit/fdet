import asyncio


class RAG:

    def __init__(self):
        pass

    def main(self, text, retriever):
        ...

    # noinspection PyRedeclaration
    def main(self, text, retriever):
        return asyncio.run(self.async_main(text, retriever))

    # [{"claim": claim, "label" : label, "supports" : percent[0], "refutes" : percent[1], "nei": percent[2],
    # "evidence" : text, "justify" : justify, "url" : url}]
    async def async_main(self, text: str, retriever):
        ...

    async def numerical_evaluation(self, justify):
        ...

    async def generate(self, claim, evidence):
        ...
