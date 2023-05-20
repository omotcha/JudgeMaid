import os
import sys

# uncomment line below if "module not found" happens
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gradio as gr
from doc_qa.tasks import Tasks
from config.webui_config import *
from config.doc_qa_config import *
from config.function_mapping import webui_mapping
from example.docqa_inputs import *
from util.format.markdown import MarkdownUtil
from multiprocessing import Manager
from threading import Thread
import time
import json
import re


def img_classifier(img):
    """
    this is example as well as default case
    :param img:
    :return:
    """
    return {
        'cat': 0.3,
        'dog': 0.7
    }


def raw_process_workflow(
        query_raw: str,
        query_yaml: str,
        task_extraction: list,
        task_classification: str or None,
        embedding_model: str or None,
        llm: str or None,
        temperature: float or None,
        max_tokens: int or None
):
    start = time.time()

    # sanity checks and naming mapping

    if len(task_extraction) == 0:
        return "", "Error: Not a valid workflow."

    task_extraction = [webui_mapping[task] for task in task_extraction]

    if len(query_raw) <= 1:
        return "", "Error: Not a valid query."

    if task_classification is None:
        return "", "Error: Not a valid classification method."

    task_classification = webui_mapping[task_classification]

    # todo: support embedding-based classification
    if task_classification == "embedding":
        return "", "Error: Current classification method not supported."

    # if task_classification == "embedding" and embedding_model is None:
    #     return "", "Error: No embedding model indicated."

    if llm is None:
        return "", "Error: No llm indicated."

    if temperature is None:
        return "", "Error: No temperature indicated."

    if max_tokens is None:
        return "", "Error: No max tokens indicated"

    perform_classification = False if task_classification == "none" else True

    # arbitrary threshold of whether to perform api doc generation or not
    perform_api_doc_generation = len(query_yaml) >= 10

    if not perform_api_doc_generation and "api doc generation" in task_extraction:
        task_extraction.remove("api doc generation")

    if perform_classification:
        if "keyword extraction" not in task_extraction or "entity recognition" not in task_extraction:
            return "", "Error: Stage 1 not completed."

    # sanity checks completed

    all_tasks = {
        "entity recognition": "entity_recognition",
        "keyword extraction": "keyword_extraction",
        "classification": "classification",
        "api doc generation": "prompt_api_doc_generation"
    }

    if allow_multithreading:
        manager = Manager()
        task_result = manager.dict()
        task_dev = manager.dict()
    else:
        task_result = {}
        task_dev = {}

    threads = []
    tasks = Tasks()

    # extraction

    if allow_multithreading:
        for k in all_tasks.keys():
            if k in task_extraction and hasattr(tasks, all_tasks[k]):
                task = getattr(tasks, all_tasks[k])
                threads.append(Thread(target=task, kwargs={
                    "context": query_yaml if k == "api doc generation" else query_raw,
                    "llm_option": llm,
                    "temperature": 0.6 if k == "api doc generation" else temperature,
                    "max_tokens": -1 if k == "api doc generation" else max_tokens,
                    "task_result": task_result,
                    "task_dev": task_dev
                }))

        for t in threads:
            t.start()

        for t in threads:
            t.join()
    else:
        for k in all_tasks.keys():
            if k in task_extraction and hasattr(tasks, all_tasks[k]):
                getattr(tasks, all_tasks[k])(
                    context=query_yaml if k == "api doc generation" else query_raw,
                    llm_option=llm,
                    temperature=0.6 if k == "api doc generation" else temperature,
                    max_tokens=-1 if k in ["api doc generation", "entity recognition"] else max_tokens,
                    task_result=task_result,
                    task_dev=task_dev
                )

    # load json as prev knowledge for next stage
    result = {}
    for task in task_extraction:
        if task in task_dev.keys() and task_dev[task] == "success":
            if task == "api doc generation":
                result[task] = task_result[task]
            else:
                trimmed = re.sub(r'\n\s+', '', task_result[task])
                try:
                    entity = json.loads(trimmed)
                    if type(entity) is dict:
                        for k, v in entity.items():
                            result[k] = v
                    else:
                        result[task] = entity
                except json.decoder.JSONDecodeError:
                    result[task] = trimmed

    # classification
    if perform_classification:
        # previous knowledge construct
        if "entity recognition" not in task_result.keys():
            task_result["classification"] = ""
            task_dev["classification"] = "Error: Stage 1 not completed."
        else:
            tasks.prompt_classification(
                prev_knowledge=result,
                llm_option=llm,
                temperature=temperature,
                max_tokens=64,
                task_result=task_result,
                task_dev=task_dev
            )

    # add classification result into json
    if "classification" in task_dev.keys() and task_dev["classification"] == "success":
        for k, v in dict(task_result["classification"]).items():
            result[k] = v

    result_text = ""
    time_count = time.time() - start
    dev_text = f"Time count: {time_count}\n"

    for task in all_tasks:
        if task in task_dev.keys() and task_dev[task] == "success":
            dev_text += task_dev[task] + "\n"

    if display_markdown:
        md_util = MarkdownUtil(None)
        result_text = md_util.dict2md(result)
    else:
        result_text += json.dumps(result, ensure_ascii=False)
    dev_text = dev_text + "\n\n" + result_text

    return result_text, dev_text


def launch():
    """
    launch a gradio user interface
    :return:
    """
    with gr.Blocks(css=block_css) as demo:
        gr.Markdown(webui_title)

        acrd_qa = gr.Accordion("输入材料")
        acrd_settings = gr.Accordion("设置")

        simple_dev_text = gr.TextArea(
            label="测试窗口",
            interactive=False
        )

        simple_dev_text.visible = display_dev_text

        with acrd_qa:
            with gr.Row():
                with gr.Column(scale=6):
                    query_raw = gr.TextArea(
                        label="1. 公司和产品描述",
                        placeholder="请输入公司和产品描述",
                        value=input_raw,
                        max_lines=13
                    ).style(container=False)
                    gr.Markdown("---")
                    query_yaml = gr.TextArea(
                        label="2. API接口描述",
                        placeholder="请输入API接口描述",
                        value=input_yaml,
                        max_lines=8
                    ).style(container=False)
                    btn_submit_raw = gr.Button("生成")
                with gr.Column(scale=10):
                    if display_markdown:
                        answer_raw = gr.Markdown(
                            value=""
                        )
                    else:
                        answer_raw = gr.TextArea(
                            label="JSON",
                            interactive=False
                        )
            # with gr.Tab("公司产品文本描述"):
            #     pass
            # with gr.Tab("pdf"):
            #     with gr.Row():
            #         with gr.Column(scale=8):
            #             query_pdf = gr.Textbox(
            #                 label="one-line query",
            #                 placeholder="One-line query supported, press enter to submit:"
            #             ).style(container=False)
            #         with gr.Column(scale=8):
            #             answer_pdf = gr.TextArea(
            #                 label="answer",
            #                 interactive=False
            #             )
            #     query_pdf.submit(
            #         img_classifier,
            #         [query_pdf],
            #         [answer_pdf]
            #     )

        with acrd_settings:
            with gr.Row():
                with gr.Column(scale=6):
                    with gr.Tab("工作流程"):
                        with gr.Column():
                            gr.Markdown("**第一步: 关键信息提取**")
                            task_extraction = gr.CheckboxGroup(
                                choices=["关键词提取", "主体识别", "API文档生成"],
                                value=["关键词提取", "主体识别", "API文档生成"],
                                label="任务",
                                interactive=True
                            )
                            gr.Markdown("**第二步: 分类**")
                            select_classification_method = gr.Radio(
                                classification_options,
                                label="分类方法",
                                value=classification_options[1],
                                interactive=True
                            )

                    with gr.Tab("模型"):
                        with gr.Row():
                            select_embedding_model = gr.Radio(
                                embedding_options,
                                label="Embedding模型",
                                value=embedding_options[2],
                                interactive=False
                            )
                        with gr.Row():
                            select_llm_model = gr.Radio(
                                llm_options,
                                label="大语言模型",
                                value=llm_options[0],
                                interactive=False
                            )

                    with gr.Tab("高级"):
                        with gr.Column():
                            gr.Markdown("**大语言模型设置**")
                            with gr.Row():
                                temperature = gr.Slider(minimum=0, maximum=1, value=0.0, label="Temperature")
                                llm_top_k = gr.Slider(minimum=0, maximum=100, step=1, value=50, label="Top K")
                                max_tokens = gr.Slider(minimum=256, maximum=2048, step=64, value=448,
                                                       label="Max Tokens")

        btn_submit_raw.click(
            raw_process_workflow,
            inputs=[
                query_raw,
                query_yaml,
                task_extraction,
                select_classification_method,
                select_embedding_model,
                select_llm_model,
                temperature,
                max_tokens
            ],
            outputs=[
                answer_raw,
                simple_dev_text
            ],
            show_progress=latent_progress
        )

    demo.launch(
        server_name=server_name,
        server_port=server_port,
        show_api=show_api,
        share=share,
        inbrowser=in_browser
    )


if __name__ == '__main__':
    launch()
