import os

from config.doc_qa_config import *
from util.knowledge.embedding import EmbeddingUtil
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from config.common import tmp_dir

target_dir = os.path.join(tmp_dir, "txt_pool")


def chain_query(query: str, knowledge_base: str) -> str:
    if llm_option != "openai":
        return ""
    else:
        llm = OpenAI(temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))
    util = EmbeddingUtil(opt=None)
    if not util.load_pdf(knowledge_base):
        return ""
    chain = load_qa_chain(llm, chain_type="stuff")
    docs = util.similarity_search(query)
    return chain.run(input_documents=docs, question=query)


if __name__ == '__main__':
    answer = chain_query(
        query="公司有什么产品？产品有什么特点？",
        knowledge_base="example.pdf"
    )
    print(answer)
