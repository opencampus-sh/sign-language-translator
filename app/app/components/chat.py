# app/components/chat.py
import gradio as gr
from config.settings import CHAT_SETTINGS
from app.models.voicetospeech_model import transcribe


def send_message_from_sign_language(message, history):
    if message:
        history.append({"role": "user", "content": message})
        return "", history


def send_message_from_other(message, history):
    if message:
        history.append({"role": "assistant", "content": message})
        return "", history


def update_button_state(text):
    return gr.update(interactive=bool(text.strip()))


def process_audio(audio, history):
    """Verarbeitet Audio-Eingabe und fügt sie zum Chat hinzu"""
    if audio is None:
        return history

    try:
        # Audio ist ein Tupel (sample_rate, audio_data)
        sample_rate = audio[0]
        audio_data = audio[1]

        text = transcribe(audio)
        if text and text.strip():  # Nur nicht-leere Transkriptionen hinzufügen
            send_message_from_other(text, history)
        return history
    except Exception as e:
        send_message_from_other("Fehler bei der Transkription", history)
        return history


def create_chat_component():
    with gr.Column():
        # Chat Verlauf
        with gr.Column(variant="panel"):
            chat_history = gr.Chatbot(
                label=CHAT_SETTINGS['label'],
                height=CHAT_SETTINGS['height'],
                value=[],
                avatar_images=None,
                render_markdown=True,
                show_label=True,
                container=True,
                type="messages",
                show_copy_button=False,
                show_share_button=False,
                bubble_full_width=False
            )

            # Audio-Eingabe
            audio_input = gr.Audio(
                sources=["microphone", "upload"],
                type="numpy",
                label="Spracheingabe",
                streaming=False,
                format="wav",
                show_download_button=False,
            )

        # Debug Accordion
        with gr.Accordion("Debug Area", open=False):
            # Gebärdensprache Input
            with gr.Row():
                sign_input = gr.Textbox(
                    label="Gebärdensprache Nachricht",
                    placeholder="Nachricht eingeben...",
                    scale=4,
                    container=True,
                    show_label=True
                )
                sign_send = gr.Button("Senden", scale=1, interactive=False, variant="primary")

            # Andere Seite Input
            with gr.Row():
                other_input = gr.Textbox(
                    label="Andere Nachricht",
                    placeholder="Nachricht eingeben...",
                    scale=4,
                    container=True,
                    show_label=True
                )
                other_send = gr.Button("Senden", scale=1, interactive=False, variant="primary")

        # Event Handler für Audio
        audio_input.change(
            fn=process_audio,
            inputs=[audio_input, chat_history],
            outputs=[chat_history]
        )

        # Bestehende Event Handler
        sign_send.click(
            fn=send_message_from_sign_language,
            inputs=[sign_input, chat_history],
            outputs=[sign_input, chat_history]
        )

        other_send.click(
            fn=send_message_from_other,
            inputs=[other_input, chat_history],
            outputs=[other_input, chat_history]
        )

        sign_input.submit(
            fn=send_message_from_sign_language,
            inputs=[sign_input, chat_history],
            outputs=[sign_input, chat_history]
        )

        other_input.submit(
            fn=send_message_from_other,
            inputs=[other_input, chat_history],
            outputs=[other_input, chat_history]
        )

        sign_input.change(
            fn=update_button_state,
            inputs=[sign_input],
            outputs=[sign_send]
        )

        other_input.change(
            fn=update_button_state,
            inputs=[other_input],
            outputs=[other_send]
        )

        return chat_history, audio_input, sign_input, sign_send, other_input, other_send
