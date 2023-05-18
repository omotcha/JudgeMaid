from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config.doc_qa_config import zh_prompts
from config.webui_config import display_format


class Tasks:
    @staticmethod
    def entity_recognition(
            context: str,
            llm_option: str,
            temperature: float,
            max_tokens: int,
            result: dict,
            dev: dict):
        """

        :param dev:
        :param result:
        :param context:
        :param llm_option:
        :param temperature:
        :param max_tokens:
        :return:
        """
        from prompt_templates.entity_recognition import prompt_entity_recognition_en, prompt_entity_recognition_zh
        if "entity recognition" in dev.keys():
            return
        if llm_option == "openai":
            llm = OpenAI(temperature=temperature, max_tokens=max_tokens)
        else:
            # todo: support more LLMs
            result["entity recognition"] = ""
            dev["entity recognition"] = "Currently only openai model supported."
            return

        prompt = PromptTemplate(
            template=prompt_entity_recognition_zh if zh_prompts else prompt_entity_recognition_en,
            input_variables=["display_format", "context"]
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        result["entity recognition"] = chain.run({"display_format": display_format, "context": context})
        dev["entity recognition"] = "success"

    @staticmethod
    def keyword_extraction(
            context: str,
            llm_option: str,
            temperature: float,
            max_tokens: int,
            result: dict,
            dev: dict):
        """

        :param dev:
        :param result:
        :param context:
        :param llm_option:
        :param temperature:
        :param max_tokens:
        :return:
        """
        from prompt_templates.keyword_extraction import prompt_keyword_extraction_en, prompt_keyword_extraction_zh
        if "keyword extraction" in dev.keys():
            return
        if llm_option == "openai":
            llm = OpenAI(temperature=temperature, max_tokens=max_tokens)
        else:
            # todo: support more LLMs
            result["keyword extraction"] = ""
            dev["keyword extraction"] = "Currently only openai model supported."
            return

        prompt = PromptTemplate(
            template=prompt_keyword_extraction_zh if zh_prompts else prompt_keyword_extraction_en,
            input_variables=["display_format", "context"]
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        result["keyword extraction"] = chain.run({"display_format": display_format, "context": context})
        dev["keyword extraction"] = "success"
