# Sign Language Translator

A real-time sign language translation application built with Python, Gradio, and machine learning technologies. This application enables communication between sign language users and others through real-time video processing, gesture recognition, and speech transcription.

## Features

- **Real-time Sign Language Detection**: Uses MediaPipe for hand, face, and pose landmark detection
- **Live Webcam Processing**: Streams and processes video input in real-time
- **Speech-to-Text**: Converts spoken language to text using OpenAI Whisper
- **Interactive Chat Interface**: Dual-sided chat for communication between users
- **Landmark Data Export**: Record and export gesture data in CSV format
- **Vertex AI Integration**: Ready for cloud-based machine learning predictions
- **Modern Web Interface**: Built with Gradio for an intuitive user experience

## Prerequisites

- Python 3.8 or higher
- Webcam or camera device
- Microphone (for speech input)
- Internet connection (for some AI features)

## Installation

1. **Clone the repository** (if not already done):

   ```bash
   git clone <your-repo-url>
   cd sign-language-translator
   ```

2. **Navigate to the app directory**:

   ```bash
   cd app
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (optional):
   Create a `.env` file in the app directory for configuration:
   ```bash
   # Google Cloud settings (for Vertex AI)
   GOOGLE_CLOUD_PROJECT=your-project-id
   GOOGLE_CLOUD_LOCATION=europe-west3
   VERTEX_AI_ENDPOINT_ID=your-endpoint-id
   ```

## Quick Start

1. **Run the application**:

   ```bash
   python main.py
   ```

2. **Access the interface**:

   - The app will automatically open in your default browser
   - If not, navigate to: `http://127.0.0.1:7860`

3. **Grant camera and microphone permissions** when prompted by your browser

## How to Use

### Main Interface

The application consists of two main components:

#### 1. Chat Component (Left Side)

- **Voice Input**: Use the microphone to speak - your speech will be automatically transcribed and added to the chat
- **Text Input**: Manually type messages using the debug area
- **Chat History**: View the conversation between both parties

#### 2. Webcam Component (Right Side)

- **Real-time Video**: Shows your camera feed with overlay annotations
- **Gesture Recognition**: Detects and highlights hand poses, facial expressions, and body postures
- **Recording Status**: Displays current recording state and frame count
- **Data Export**: Download recorded landmark data as CSV files

### Configuration Options

You can adjust detection settings by modifying the global variables in `source/components/webcam.py`:

```python
face_detail_live = "minimal"    # Options: "none", "minimal", "detailed"
hand_detail_live = "basic"      # Options: "none", "basic", "detailed"
pose_detail_live = "none"       # Options: "none", "basic", "detailed"
```

### Debug Features

Expand the "Debug Area" accordions to access:

- Manual text input for testing
- Detailed landmark data preview
- CSV data download
- Processing statistics

## Project Structure

```
app/
├── main.py                     # Application entry point
├── requirements.txt            # Python dependencies
├── vertex_ai_client.py        # Google Cloud Vertex AI integration
├── __init__.py                # Package initialization
│
├── config/                     # Configuration files
│   ├── settings.py            # Main application settings
│   └── development.py         # Development-specific config
│
├── source/                     # Core application code
│   ├── interface.py           # Main Gradio interface setup
│   ├── components/            # UI components
│   │   ├── chat.py           # Chat interface component
│   │   └── webcam.py         # Webcam processing component
│   └── models/               # Machine learning models
│       ├── transcriber.py    # Audio transcription logic
│       ├── voicetospeech_model.py  # Speech-to-text model
│       └── mediapipe_model.py     # MediaPipe gesture detection
│
├── static/                    # Static assets
│   ├── images/               # Image assets
│   └── styles/               # CSS stylesheets
│
└── instance/                  # Instance-specific files
```

## Key Technologies

- **[Gradio](https://gradio.app/)**: Web interface framework
- **[MediaPipe](https://mediapipe.dev/)**: Real-time pose and gesture detection
- **[OpenAI Whisper](https://openai.com/research/whisper)**: Speech recognition
- **[Google Cloud Vertex AI](https://cloud.google.com/vertex-ai)**: Machine learning platform
- **[NumPy](https://numpy.org/)**: Numerical computing
- **[Pandas](https://pandas.pydata.org/)**: Data manipulation
- **[Librosa](https://librosa.org/)**: Audio processing

## Development

### Running in Development Mode

The application runs in debug mode by default, which enables:

- Automatic reloading on code changes
- Detailed error messages
- Enhanced logging

### Adding New Features

1. **New UI Components**: Add to `source/components/`
2. **New Models**: Add to `source/models/`
3. **Configuration**: Update `config/settings.py`
4. **Static Assets**: Place in `static/` directory

### Error Handling

The application includes comprehensive error handling:

- Graceful degradation when camera/microphone unavailable
- Fallback processing for failed AI predictions
- Detailed logging for debugging

## Troubleshooting

### Common Issues

1. **Camera not working**:

   - Ensure camera permissions are granted in browser
   - Check if camera is being used by another application
   - Try refreshing the page

2. **Audio transcription failing**:

   - Verify microphone permissions
   - Check audio input levels
   - Ensure stable internet connection

3. **Slow performance**:
   - Reduce detection detail levels in configuration
   - Close other resource-intensive applications
   - Ensure adequate system resources

### Log Files

Check the console output for detailed error messages and debugging information.

## Configuration

### Interface Settings

Modify `config/settings.py` to customize:

- Interface title and header
- Component dimensions
- File paths and directories
- Detection sensitivity

### Performance Tuning

Adjust these settings for better performance:

- Lower MediaPipe model complexity
- Reduce video resolution
- Adjust processing frame rate

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues and questions:

- Check the troubleshooting section above
- Review the console logs for error details
- [Add your contact/support information]

---

**Note**: This application processes video and audio data locally for privacy. Vertex AI integration is optional and can be disabled by not configuring the cloud credentials.
