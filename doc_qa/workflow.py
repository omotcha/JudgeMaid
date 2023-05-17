from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config.doc_qa_config import zh_prompts


def entity_recognition(context: str, llm_option: str, temperature: float, max_tokens: int) -> tuple[str, str]:
    """

    :param context:
    :param llm_option:
    :param temperature:
    :param max_tokens:
    :return:
    """
    from prompt_templates.entity_recognition import prompt_entity_recognition_en, prompt_entity_recognition_zh
    if llm_option == "openai":
        llm = OpenAI(temperature=temperature, max_tokens=max_tokens)
    else:
        # todo: support more LLMs
        return "", "Currently only openai model supported"

    prompt = PromptTemplate(
        template=prompt_entity_recognition_zh if zh_prompts else prompt_entity_recognition_en,
        input_variables=["context"]
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    result = chain.run(context)
    return result, "success"
