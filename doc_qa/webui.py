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
        temperature: float or None
):
    if workflow == "keyword extraction":
        if len(query) <= 1:
            return "", "Error: Not a valid query."
        if llm is None:
            return "", "Error: No llm indicated."
        if temperature is None:
            return "", "Error: No temperature indicated."
        result, dev = keyword_extraction(context=query, llm_option=llm, temperature=temperature)
        return result, dev
    else:
        return "", "Error: Not a valid workflow."


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
                            select_base_task = gr.Radio(
                                task_options,
                                label="Base Task",
                                value=task_options[0],
                                interactive=True
                            )
                    with gr.Tab("Advanced"):
                        with gr.Row():
                            temperature = gr.Slider(minimum=0, maximum=1, value=0.0, label="Temperature")
                            llm_top_k = gr.Slider(minimum=0, maximum=100, step=1, value=50, label="Top K")

        btn_submit.click(
            raw_process,
            inputs=[query_raw, select_base_task, select_embedding_model, select_llm_model, temperature],
            outputs=[answer_raw, simple_dev_text],
            show_progress=latent_progress
        )

    demo.queue(concurrency_count=concurrency_cnt).launch(
        server_name=server_name,
        server_port=server_port,
        show_api=show_api,
        share=share,
        inbrowser=in_browser
    )


if __name__ == '__main__':
    launch()
