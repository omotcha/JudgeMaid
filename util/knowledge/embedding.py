import os

import torch
from transformers import AutoTokenizer, AutoModel
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.embeddings.huggingface_hub import HuggingFaceHubEmbeddings
from langchain.vectorstores import FAISS
from config.doc_qa_config import *
from config.common import tmp_dir

target_dir = os.path.join(tmp_dir, "txt_pool")


def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


class EmbeddingUtil:
    def __init__(self):
        # init embedding option
        if embedding_option == "openai":
            self._embeddings = OpenAIEmbeddings()
        elif embedding_option == "text2vec-cn":
            self._tokenizer = AutoTokenizer.from_pretrained("GanymedeNil/text2vec-large-chinese")
            self._model = AutoModel.from_pretrained("GanymedeNil/text2vec-large-chinese")
            self._embeddings = HuggingFaceEmbeddings(
                model_name="GanymedeNil/text2vec-large-chinese"
            )
        else:
            self._embeddings = HuggingFaceHubEmbeddings(
                repo_id="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
                task="feature-extraction",
                huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
            )
        # init knowledge base
        self._db = None

    def load_txt(self, fin: str or os.PathLike):
        """
        load a text file as knowledge base
        :param fin:
        :return:
        """
        documents = TextLoader(os.path.join(target_dir, fin), encoding="utf-8").load()
        text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        docs = text_splitter.split_documents(documents)
        self._db = FAISS.from_documents(docs, self._embeddings)

    def similar_search(self, query: str) -> list or None:
        if self._db is None:
            return None
        docs = self._db.similarity_search(query)
        return docs

    def embed_query(self, query):
        if embedding_option == "openai":
            return None
        elif embedding_option == "text2vec-cn":
            encoded_input = self._tokenizer(query, padding=True, truncation=True, return_tensors='pt')
            with torch.no_grad():
                model_output = self._model(**encoded_input)
            sentence_embedding = mean_pooling(model_output, encoded_input['attention_mask'])
            return sentence_embedding
        else:
            return self._embeddings.embed_query(query)


if __name__ == '__main__':
    util = EmbeddingUtil()
    util.load_txt("01_split.txt")
    print(util.similar_search("公司名称是什么？"))
    print(util.similar_search("产品名称是什么？"))
    # print(util.embed_query("公司名称是什么？"))
