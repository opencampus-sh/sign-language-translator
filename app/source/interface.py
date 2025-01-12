import gradio as gr

import config.settings
from source.components.chat import create_chat_component
from source.components.webcam import create_webcam_component
from config.settings import INTERFACE_SETTINGS


def create_interface():

    with gr.Blocks(

        title=INTERFACE_SETTINGS['title'],
        theme=gr.themes.Soft(),
        css_paths=[INTERFACE_SETTINGS['css_file']]

    ) as interface:

        gr.Markdown(INTERFACE_SETTINGS.get('header', ''))
        with gr.Row(variant="panel"):
            with gr.Row():
                # Chat-Komponente (linke Seite)
                with gr.Column(scale=1):
                    chat_component = create_chat_component()

                # Webcam-Komponente (rechte Seite)
                with gr.Column(scale=1):
                    webcam_component = create_webcam_component()

    return interface
