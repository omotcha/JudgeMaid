# the embedding model option, "openai"/"text2vec-cn"/"sentence-transformers"
# currently for test, try "openai" first
embedding_options = ["openai", "text2vec-cn", "sentence-transformers"]
embedding_option = "sentence-transformers"

# text splitter options
chunk_size = 1000
chunk_overlap = 0

# top-k ranked similarity
top_k = 3

# the llm option, "openai"/"glm"/"llama"
# currently only "openai" supported
llm_options = ["openai"]
llm_option = "openai"

# source file format option, "pdf"/"text"
# currently for test, try "text" first
src_fmt_options = ["pdf", "text"]
src_fmt = ["text"]
