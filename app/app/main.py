import os
import sys
import config

# Füge den Projektroot zum Python-Pfad hinzu
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from app.interface import create_interface


def main():
    interface = create_interface()
    interface.launch(
        allowed_paths=[config.settings.STATIC_DIR],
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        debug=True,
        inbrowser=True,
        show_error=True
    )


if __name__ == "__main__":
    main()
