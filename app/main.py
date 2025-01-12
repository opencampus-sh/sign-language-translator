# main.py

import os
import sys
import config

# Füge den Projektroot zum Python-Pfad hinzu, falls nötig
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from source.interface import create_interface


def create_app():
    """Factory function to create the Gradio application."""
    app = create_interface()
    app.launch(
        allowed_paths=[config.settings.STATIC_DIR],
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        debug=True,
        inbrowser=True,
        show_error=True,
    )
    return app


def main():
    """Main function to start the application."""
    try:
        create_app()
    except Exception as e:
        import logging
        logging.error(f"An error occurred while starting the app: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
