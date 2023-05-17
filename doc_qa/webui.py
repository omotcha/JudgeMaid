import gradio as gr
from doc_qa.workflow import *
from config.webui_config import *
from config.doc_qa_config import *


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


def raw_process(
        query: str,
        workflow: str,
        embedding_model: str or None,
        llm: str or None,
        temperature: float or None,
        max_tokens: int or None
):
    if workflow == "keyword extraction":
        if len(query) <= 1:
            return "", "Error: Not a valid query."
        if llm is None:
            return "", "Error: No llm indicated."
        if temperature is None:
            return "", "Error: No temperature indicated."
        if max_tokens is None:
            return "", "Error: No max tokens indicated"
        result, dev = entity_recognition(context=query, llm_option=llm, temperature=temperature, max_tokens=-1)
        return result, dev
    else:
        return "", "Error: Not a valid workflow."


def raw_process_workflow(
        query: str,
        workflow: list,
        embedding_model: str,
        llm: str or None,
        temperature: float or None,
        max_tokens: int or None
):
    # sanity checks
    if len(workflow) == 0:
        return "", "Error: Not a valid workflow."
    if len(query) <= 1:
        return "", "Error: Not a valid query."
    if llm is None:
        return "", "Error: No llm indicated."
    if temperature is None:
        return "", "Error: No temperature indicated."
    if max_tokens is None:
        return "", "Error: No max tokens indicated"

    result = ""
    dev = ""
    # workflow: currently only support sync workflow
    # todo: async workflow
    if "keyword extraction" in workflow:
        pass
    if "entity recognition" in workflow:
        result_delta, dev_delta = entity_recognition(context=query, llm_option=llm, temperature=temperature, max_tokens=-1)
        if dev_delta == "success":
            result += result_delta + "\n"
        dev += dev_delta + "\n"
    return result, dev


def change_embedding_model(embedding_model):
    return embedding_model


def launch():
    """
    launch a gradio user interface
    :return:
    """
    with gr.Blocks(css=block_css) as demo:
        gr.Markdown(webui_title)

        acrd_qa = gr.Accordion("QA")
        acrd_settings = gr.Accordion("Settings")
        # acrd_dev = gr.Accordion("Dev")

        simple_dev_text = gr.TextArea(
            label="dev output",
            interactive=False
        )

        with acrd_qa:
            with gr.Tab("raw"):
                with gr.Row():
                    with gr.Column(scale=8):
                        query_raw = gr.TextArea(
                            label="query",
                            placeholder="Raw text supported, try markdown first:"
                        ).style(container=False)
                        btn_submit = gr.Button("Submit")
                    with gr.Column(scale=8):
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

        with acrd_settings:
            with gr.Row():
                with gr.Column(scale=6):
                    with gr.Tab("Models & Workflow"):
                        with gr.Row():
                            select_embedding_model = gr.Radio(
                                embedding_options,
                                label="Supported Embedding Models",
                                value=embedding_options[2],
                                interactive=True
                            )
                            select_embedding_model.change(
                                fn=change_embedding_model,
                                inputs=[select_embedding_model],
                                outputs=[simple_dev_text]
                            )
                        with gr.Row():
                            select_llm_model = gr.Radio(
                                llm_options,
                                label="Supported LLMs",
                                value=llm_options[0],
                                interactive=False
                            )
                        with gr.Row():
                            workflow = gr.CheckboxGroup(
                                choices=["keyword extraction", "entity recognition"],
                                label="Workflow(Tasks)",
                                interactive=True
                            )
                            select_base_task = gr.Radio(
                                task_options,
                                label="Workflow",
                                value=task_options[0],
                                interactive=True
                            )
                    with gr.Tab("Advanced"):
                        with gr.Row():
                            temperature = gr.Slider(minimum=0, maximum=1, value=0.0, label="Temperature")
                            llm_top_k = gr.Slider(minimum=0, maximum=100, step=1, value=50, label="Top K")
                            max_tokens = gr.Slider(minimum=256, maximum=2048, step=256, value=512, label="Max Tokens")

        # btn_submit.click(
        #     raw_process,
        #     inputs=[query_raw, select_base_task, select_embedding_model, select_llm_model, temperature, max_tokens],
        #     outputs=[answer_raw, simple_dev_text],
        #     show_progress=latent_progress
        # )
        btn_submit.click(
            raw_process_workflow,
            inputs=[query_raw, workflow, select_embedding_model, select_llm_model, temperature, max_tokens],
            outputs=[answer_raw, simple_dev_text],
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
