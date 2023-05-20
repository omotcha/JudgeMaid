# the embedding model option, "openai"/"text2vec-cn"/"sentence-transformers"
# currently for test, try "openai" first
embedding_options = ["openai", "text2vec-cn", "sentence-transformers"]
embedding_option = "sentence-transformers"

# the classification option, "prompt"/"embedding"/"fine-tuned"(not supported yet)
classification_options = ["不执行分类", "基于提示分类"]
classification_option = "基于提示分类"

# text splitter options
chunk_size = 1000
chunk_overlap = 0

# top-k ranked similarity
top_k = 3

# the llm option, "openai"/"glm"/"llama"
# currently only "openai" supported
llm_options = ["openai", "glm", "llama"]
llm_option = "openai"

# source file format option, "pdf"/"text"
# currently for test, try "text" first
src_fmt_options = ["pdf", "text"]
src_fmt = "text"

# task option
task_options = ["keyword extraction"]
task_option = "keyword extraction"

# prompt language, default True for Chinese prompt template, false for English prompt template
# zh_prompts = False
