from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
# from config.doc_qa_config import zh_prompts


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
            # template=prompt_entity_recognition_zh if zh_prompts else prompt_entity_recognition_en,
            template=prompt_entity_recognition_en,
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
            # template=prompt_keyword_extraction_zh if zh_prompts else prompt_keyword_extraction_en,
            template=prompt_keyword_extraction_en,
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
        from prompt_templates.classification import prompt_multiple_classification_zh, prompt_binary_classification_zh, classification_tasks

        # in case classification task has been performed
        if "classification" in task_dev.keys():
            return
        if llm_option == "openai":
            llm = OpenAI(temperature=temperature, max_tokens=max_tokens)
        else:
            # todo: support more LLMs
            task_result["classification"] = ""
            task_dev["classification"] = "Currently only openai model supported."
            return

        tmp = {}
        for k, v in classification_tasks.items():
            top_k = v["top_k"]
            if top_k is None:
                prompt = PromptTemplate(
                    template=prompt_binary_classification_zh,
                    input_variables=["intro", "company_name", "company_description", "product_name", "classes"]
                )
            else:
                prompt = PromptTemplate(
                    template=prompt_multiple_classification_zh,
                    input_variables=["top_k", "intro", "company_name", "company_description", "product_name", "classes"]
                )
            intro = "" if v["intro"] is None else v["intro"]
            company_name = prev_knowledge["company name"]
            company_description = prev_knowledge["company description"]
            product_name = prev_knowledge["product name"]
            classes = v["classes"]
            chain = LLMChain(llm=llm, prompt=prompt)
            if top_k is None:
                tmp[k] = chain.run({
                    "intro": intro,
                    "company_name": company_name,
                    "company_description": company_description,
                    "product_name": product_name[0] if product_name is list else product_name,
                    "classes": classes
                })
            else:
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

    @staticmethod
    def prompt_yaml2md(
            context: str,
            llm_option: str,
            temperature: float,
            max_tokens: int,
            task_result: dict,
            task_dev: dict
    ):
        """

        :param context:
        :param llm_option:
        :param temperature:
        :param max_tokens:
        :param task_result:
        :param task_dev:
        :return:
        """
        from prompt_templates.yaml2md import prompt_yaml2md_en

        # in case yaml2md task has been performed
        if "yaml2md" in task_dev.keys():
            return
        if llm_option == "openai":
            llm = OpenAI(temperature=temperature, max_tokens=max_tokens)
        else:
            # todo: support more LLMs
            task_result["yaml2md"] = ""
            task_dev["yaml2md"] = "Currently only openai model supported."
            return

        prompt = PromptTemplate(
                    template=prompt_yaml2md_en,
                    input_variables=["context"]
        )

        chain = LLMChain(llm=llm, prompt=prompt)
        task_result["yaml2md"] = chain.run({"context": context})
        task_dev["yaml2md"] = "success"

