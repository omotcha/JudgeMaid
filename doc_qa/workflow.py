from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

prompt_template = """下面文字介绍了某公司及其产品，请根据要求从中提取关键信息，并用json的形式来描述。
    若无法从中得到答案，请说"没有提供足够的相关信息"，不允许在答案中添加编造成分。答案请使用中文。

    公司及产品介绍:
    {context}

    关键信息：
    公司名称，公司描述，产品名称(如果有多个产品，请列举)，产品关键词
    """


def keyword_extraction(context: str, llm_option: str, temperature: float) -> tuple[str, str]:
    if llm_option == "openai":
        llm = OpenAI(temperature=temperature)
    else:
        # todo: support more LLMs
        return "", "Currently only openai model supported"

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context"]
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    result = chain.run(context)
    return result, "Success"
