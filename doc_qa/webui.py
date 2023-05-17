import gradio as gr
from config.webui_config import *
from config.doc_qa_config import *


def img_classifier(img):
    return {
        'cat': 0.3,
        'dog': 0.7
    }


def change_embedding_model(embedding_model):
    return embedding_model


def launch():
    """
    launch a gradio user interface
    :return:
    """
    with gr.Blocks(css=block_css) as demo:
        gr.Markdown(webui_title)
        fmt_opt, embedding_opt, llm_opt = gr.State(src_fmt_options), gr.State(embedding_options), gr.State(llm_options)

        acrd_qa = gr.Accordion("QA")
        acrd_settings = gr.Accordion("Settings")
        # acrd_dev = gr.Accordion("Dev")

        simple_dev_text = gr.Textbox(
            label="dev output",
            interactive=False
        )

        with acrd_qa:
            with gr.Tab("raw text"):
                with gr.Row():
                    with gr.Column(scale=8):
                        query = gr.Textbox(
                            label="query",
                            placeholder="Raw text supported, try markdown first:"
                        ).style(container=False)
                        btn_submit = gr.Button("Submit")
                    with gr.Column(scale=8):
                        answer = gr.Textbox(
                            label="answer",
                            interactive=False
                        )
                btn_submit.click(
                    img_classifier,
                    inputs=[query],
                    outputs=[answer],
                    show_progress=latent_progress
                )
            with gr.Tab("pdf"):
                with gr.Row():
                    with gr.Column(scale=8):
                        query = gr.Textbox(
                            label="one-line query",
                            placeholder="One-line query supported, press enter to submit:"
                        ).style(container=False)
                    with gr.Column(scale=8):
                        answer = gr.Textbox(
                            label="answer",
                            interactive=False
                        )
                query.submit(
                    img_classifier,
                    [query],
                    [answer]
                )

        with acrd_settings:
            with gr.Row():
                with gr.Column(scale=6):
                    with gr.Tab("Models"):
                        with gr.Row():
                            select_embedding_model = gr.Radio(
                                embedding_options,
                                label="Supported Embedding Models"
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
                with gr.Column(scale=6):
                    with gr.Tab("Tasks"):
                        with gr.Row():
                            select_base_task = gr.Radio(
                                ["a", "b"],
                                label="Base task"
                            )

        # with acrd_dev:
        #     with gr.Row():
        #         with gr.Column(scale=8):

    demo.queue(concurrency_count=concurrency_cnt).launch(
        server_name=server_name,
        server_port=server_port,
        show_api=show_api,
        share=share,
        inbrowser=in_browser
    )


if __name__ == '__main__':
    launch()
