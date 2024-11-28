#!/bin/bash

# Check for required tools
command -v python3 >/dev/null 2>&1 || { echo "Python 3 is required but not installed."; exit 1; }
command -v gcloud >/dev/null 2>&1 || { echo "Google Cloud SDK is required but not installed."; exit 1; }

# Set up Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r app/requirements.txt
pip install -r app/requirements-dev.txt  # Development-specific requirements

# Configure gcloud
PROJECT_ID=$(gcloud config get-value project)
if [ -z "$PROJECT_ID" ]; then
    echo "Please run 'gcloud init' to configure your project"
    exit 1
fi

# Set up environment variables
cat > .env << EOL
GCP_PROJECT_ID=${PROJECT_ID}
GCP_LOCATION=europe-west3
USE_MOCK_MODEL=true
PYTHONPATH=./app
EOL

# Create development configuration
mkdir -p app/instance
cp app/config/development.py app/instance/config.py

echo "Development environment setup complete!"
echo "To activate the environment:"
echo "  source venv/bin/activate"
echo "To use mock model (offline development):"
echo "  export USE_MOCK_MODEL=true"
echo "To use Vertex AI endpoint:"
echo "  export USE_MOCK_MODEL=false"
echo "  export VERTEX_AI_ENDPOINT_ID=<your-endpoint-id>" 