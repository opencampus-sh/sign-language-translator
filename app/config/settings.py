import os

# Pfade
STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
IMAGES_DIR = os.path.join(STATIC_DIR, 'images')
STYLES_DIR = os.path.join(STATIC_DIR, 'styles')

# Interface Einstellungen
INTERFACE_SETTINGS = {
    'title': 'Sign Language Chat',
    'header': """
    # Sign Language Chat Interface
    """,
    'theme': 'glass',
    'background_image': "url(" + os.path.join(IMAGES_DIR, 'background.png') + ")",
    'css_file':  os.path.join(STYLES_DIR, 'style.css'),
    'debug': True
}

# Chat Einstellungen
CHAT_SETTINGS = {
    'label': 'Chat-Verlauf',
    'height': 480,
    'avatar_paths': [
        os.path.join(IMAGES_DIR, 'avatar1.png'),  # sign avatar
        os.path.join(IMAGES_DIR, 'avatar2.png')  # other avatar
    ]
}

# Webcam Einstellungen
WEBCAM_SETTINGS = {
    'label': 'Webcam Feed',
    'height': 480,
    'streaming': True,
    'mirror': True
}
