import gradio as gr
from doc_qa.tasks import Tasks
from config.webui_config import *
from config.doc_qa_config import *
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

    # sanity checks start

    if len(task_extraction) == 0:
        return "", "Error: Not a valid workflow."

    if len(query_raw) <= 1:
        return "", "Error: Not a valid query."

    if task_classification is None:
        return "", "Error: Not a valid classification method."

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
                    max_tokens=-1 if k == "api doc generation" else max_tokens,
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


def yaml_process_workflow(
        query: str,
        llm: str or None,
        temperature: float or None,
        max_tokens: int or None
):
    """
    yaml -> api doc(markdown)
    :param query:
    :param llm:
    :param temperature:
    :param max_tokens:
    :return:
    """
    start = time.time()

    # sanity checks start

    if len(query) <= 1:
        return "", "Error: Not a valid query."

    if llm is None:
        return "", "Error: No llm indicated."

    if temperature is None:
        return "", "Error: No temperature indicated."

    if max_tokens is None:
        return "", "Error: No max tokens indicated"

    # sanity checks completed

    tasks = Tasks()
    task_result = {}
    task_dev = {}

    tasks.prompt_api_doc_generation(
        context=query,
        llm_option=llm,
        temperature=0.6,
        max_tokens=-1,
        task_result=task_result,
        task_dev=task_dev
    )

    result_text = task_result["api doc generation"]
    time_count = time.time() - start
    dev_text = f"Time count: {time_count}\n"
    return result_text, dev_text


def launch():
    """
    launch a gradio user interface
    :return:
    """
    with gr.Blocks(css=block_css) as demo:
        gr.Markdown(webui_title)

        acrd_qa = gr.Accordion("QA")
        acrd_settings = gr.Accordion("Settings")

        simple_dev_text = gr.TextArea(
            label="dev output",
            interactive=False
        )

        with acrd_qa:
            with gr.Tab("raw"):
                with gr.Row():
                    with gr.Column(scale=6):
                        query_raw = gr.TextArea(
                            label="query",
                            placeholder="Raw text supported, try markdown first:"
                        ).style(container=False)
                        btn_submit_raw = gr.Button("Submit")
                    with gr.Column(scale=10):
                        if display_markdown:
                            answer_raw = gr.Markdown(
                                value=""
                            )
                        else:
                            answer_raw = gr.TextArea(
                                label="answer",
                                interactive=False
                            )
            with gr.Tab("pdf"):
                with gr.Row():
                    with gr.Column(scale=8):
                        query_pdf = gr.Textbox(
                            label="one-line query",
                            placeholder="One-line query supported, press enter to submit:"
                        ).style(container=False)
                    with gr.Column(scale=8):
                        answer_pdf = gr.TextArea(
                            label="answer",
                            interactive=False
                        )
                query_pdf.submit(
                    img_classifier,
                    [query_pdf],
                    [answer_pdf]
                )
            with gr.Tab("yaml"):
                with gr.Row():
                    with gr.Column(scale=6):
                        query_yaml = gr.TextArea(
                            label="yaml query",
                            placeholder="arbitrary yaml supported, try standard openapi first:"
                        ).style(container=False)
                        btn_submit_yaml = gr.Button("Submit")
                    with gr.Column(scale=10):
                        if display_markdown:
                            answer_yaml = gr.Markdown(
                                value=""
                            )
                        else:
                            answer_yaml = gr.TextArea(
                                label="answer",
                                interactive=False
                            )
        with acrd_settings:
            with gr.Row():
                with gr.Column(scale=6):
                    with gr.Tab("Workflow"):
                        with gr.Column():
                            gr.Markdown("**stage 1: extraction**")
                            task_extraction = gr.CheckboxGroup(
                                choices=["keyword extraction", "entity recognition", "api doc generation"],
                                label="Tasks",
                                interactive=True
                            )
                            gr.Markdown("**stage 2: classification**")
                            select_classification_method = gr.Radio(
                                classification_options,
                                label="Supported Classification Methods",
                                value=classification_options[0],
                                interactive=True
                            )

                    with gr.Tab("Models"):
                        with gr.Row():
                            select_embedding_model = gr.Radio(
                                embedding_options,
                                label="Supported Embedding Models",
                                value=embedding_options[2],
                                interactive=True
                            )
                        with gr.Row():
                            select_llm_model = gr.Radio(
                                llm_options,
                                label="Supported LLMs",
                                value=llm_options[0],
                                interactive=False
                            )

                    with gr.Tab("Advanced"):
                        with gr.Column():
                            gr.Markdown("**LLM settings**")
                            with gr.Row():
                                temperature = gr.Slider(minimum=0, maximum=1, value=0.0, label="Temperature")
                                llm_top_k = gr.Slider(minimum=0, maximum=100, step=1, value=50, label="Top K")
                                max_tokens = gr.Slider(minimum=256, maximum=2048, step=128, value=384,
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
        btn_submit_yaml.click(
            yaml_process_workflow,
            inputs=[
                query_yaml,
                select_llm_model,
                temperature,
                max_tokens
            ],
            outputs=[
                answer_yaml,
                simple_dev_text
            ]
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
