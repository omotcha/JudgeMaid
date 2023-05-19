from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config.doc_qa_config import zh_prompts


class Tasks:
    @staticmethod
    def entity_recognition(
            context: str,
            llm_option: str,
            temperature: float,
            max_tokens: int,
            task_result: dict,
            task_dev: dict):
        """

        :param task_dev:
        :param task_result:
        :param context:
        :param llm_option:
        :param temperature:
        :param max_tokens:
        :return:
        """
        from prompt_templates.entity_recognition import prompt_entity_recognition_en, prompt_entity_recognition_zh
        if "entity recognition" in task_dev.keys():
            return
        if llm_option == "openai":
            llm = OpenAI(temperature=temperature, max_tokens=max_tokens)
        else:
            # todo: support more LLMs
            task_result["entity recognition"] = ""
            task_dev["entity recognition"] = "Currently only openai model supported."
            return

        prompt = PromptTemplate(
            template=prompt_entity_recognition_zh if zh_prompts else prompt_entity_recognition_en,
            input_variables=["context"]
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        task_result["entity recognition"] = chain.run({"context": context})
        task_dev["entity recognition"] = "success"

    @staticmethod
    def keyword_extraction(
            context: str,
            llm_option: str,
            temperature: float,
            max_tokens: int,
            task_result: dict,
            task_dev: dict):
        """

        :param task_dev:
        :param task_result:
        :param context:
        :param llm_option:
        :param temperature:
        :param max_tokens:
        :return:
        """
        from prompt_templates.keyword_extraction import prompt_keyword_extraction_en, prompt_keyword_extraction_zh
        if "keyword extraction" in task_dev.keys():
            return
        if llm_option == "openai":
            llm = OpenAI(temperature=temperature, max_tokens=max_tokens)
        else:
            # todo: support more LLMs
            task_result["keyword extraction"] = ""
            task_dev["keyword extraction"] = "Currently only openai model supported."
            return

        prompt = PromptTemplate(
            template=prompt_keyword_extraction_zh if zh_prompts else prompt_keyword_extraction_en,
            input_variables=["context"]
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        task_result["keyword extraction"] = chain.run({"context": context})
        task_dev["keyword extraction"] = "success"

    @staticmethod
    def prompt_classification(
            prev_knowledge: dict,
            llm_option: str,
            temperature: float,
            max_tokens: int,
            task_result: dict,
            task_dev: dict):
        """

        :param prev_knowledge:
        :param llm_option:
        :param temperature:
        :param max_tokens:
        :param task_result:
        :param task_dev:
        :return:
        """
        from prompt_templates.classification import prompt_classification_zh, classification_tasks
        if "classification" in task_dev.keys():
            return
        if llm_option == "openai":
            llm = OpenAI(temperature=temperature, max_tokens=max_tokens)
        else:
            # todo: support more LLMs
            task_result["classification"] = ""
            task_dev["classification"] = "Currently only openai model supported."
            return

        prompt = PromptTemplate(
            template=prompt_classification_zh,
            input_variables=["top_k", "intro", "company_name", "company_description", "product_name", "classes"]
        )
        tmp = {}
        for k, v in classification_tasks.items():
            top_k = v["top_k"]
            intro = "" if v["intro"] is None else v["intro"]
            company_name = prev_knowledge["company_name"]
            company_description = prev_knowledge["company_description"]
            product_name = prev_knowledge["product_name"]
            classes = v["classes"]
            chain = LLMChain(llm=llm, prompt=prompt)
            tmp[k] = chain.run({
                "top_k": top_k,
                "intro": intro,
                "company_name": company_name,
                "company_description": company_description,
                "product_name": product_name[0] if product_name is list else product_name,
                "classes": classes
            })
        task_result["classification"] = tmp
        task_dev["classification"] = "success"
