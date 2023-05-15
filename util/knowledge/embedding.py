import os

from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings.huggingface_hub import HuggingFaceHubEmbeddings
from langchain.vectorstores import FAISS
from config.doc_qa_config import *
from config.common import tmp_dir

target_dir = os.path.join(tmp_dir, "txt_pool")


class EmbeddingUtil:
    def __init__(self):
        # init embedding option
        if embedding_option == "openai":
            self._embeddings = OpenAIEmbeddings()
        else:
            self._embeddings = None
        # init knowledge base
        self._db = None

    def load_txt(self, fin: str or os.PathLike):
        """
        load a text file as knowledge base
        :param fin:
        :return:
        """
        documents = TextLoader(os.path.join(target_dir, fin)).load()
        text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        docs = text_splitter.split_documents(documents)
        self._db = FAISS.from_documents(docs, self._embeddings)

    def similar_search(self, query: str) -> list or None:
        if self._db is None:
            return None
        docs = self._db.similarity_search(query)
        return docs


if __name__ == '__main__':
    util = EmbeddingUtil()
    print(util.similar_search("公司名称是什么？"))
