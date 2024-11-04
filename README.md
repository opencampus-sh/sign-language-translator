# Sign Language Translator

This project provides a sign language translation service using MediaPipe for keypoint extraction and a fine-tuned Whisper model for translation. The service is deployed on Google Cloud Run and managed with Terraform.

## Documentation

- [Data Access and Dataset Information](app/docs/DATA.md)
- [Model Training Guide](app/docs/TRAINING.md)
- [Deployment Scenarios](app/docs/DEPLOYMENT.md)

## Project Structure

```
sign-language-translator/
├── app/                  # Application code
├── terraform/           # Infrastructure as Code
│   ├── environments/    # Environment-specific configs
│   └── modules/         # Reusable Terraform modules
├── build/              # Build configurations
└── setup/              # Setup scripts
```

## Prerequisites

- Google Cloud SDK
- Terraform
- Python 3.9+
- Docker
- (Optional) Hugging Face account and access token for the real model

## Getting Started

1. Initialize the GCP project:

```bash
./setup/init-gcp-project.sh
```

2. Set up infrastructure:

```bash
cd terraform/environments/dev
terraform init
terraform plan
terraform apply
```

## Development Options

### Local Development

1. **Mock Model** (Default)

```bash
# Option 1: Default behavior
python app/main.py

# Option 2: Explicit mock configuration
export USE_MOCK_MODEL=true
python app/main.py
```

2. **Real Model**

```bash
export USE_MOCK_MODEL=false
export HUGGINGFACE_TOKEN=your_token_here
export MODEL_PATH=your-org/sign-language-translator
python app/main.py
```

### Docker Development

1. **Mock Model**

```bash
docker build -t sign-language-translator ./app
docker run -p 8080:8080 sign-language-translator
```

2. **Real Model**

```bash
docker build -t sign-language-translator ./app
docker run -p 8080:8080 \
  -e USE_MOCK_MODEL=false \
  -e HUGGINGFACE_TOKEN=your_token_here \
  -e MODEL_PATH=your-org/sign-language-translator \
  sign-language-translator
```

## Deployment

### Mock Model Deployment

```hcl
module "cloudrun" {
  source      = "../../modules/cloudrun"
  project_id  = var.project_id
  region      = var.region
  environment = "dev"

  env_variables = {
    USE_MOCK_MODEL = "true"
  }
}
```

### Production Model Deployment

```hcl
module "cloudrun" {
  source      = "../../modules/cloudrun"
  project_id  = var.project_id
  region      = var.region
  environment = "dev"

  env_variables = {
    USE_MOCK_MODEL = "false"
    MODEL_PATH     = "your-org/sign-language-translator"
  }

  secrets = {
    HUGGINGFACE_TOKEN = {
      secret_id = "huggingface-token-dev"
      version   = "latest"
    }
  }
}
```

## Testing the API

1. **Health Check**

```bash
curl http://localhost:8080/health
```

2. **Process Video**

```bash
curl -X POST -F "video=@path/to/your/video.mp4" http://localhost:8080/process-sign-language
```

## Environment Variables

| Variable          | Description                          | Default                           |
| ----------------- | ------------------------------------ | --------------------------------- |
| USE_MOCK_MODEL    | Use mock model instead of real model | true                              |
| HUGGINGFACE_TOKEN | Token for accessing HF model         | None                              |
| MODEL_PATH        | Path to HF model                     | your-org/sign-language-translator |
| PORT              | Port for the application             | 8080                              |

## Infrastructure Components

- Cloud Run service for the application
- Artifact Registry for container images
- Secret Manager for Hugging Face token
- IAM configurations for service accounts
- Monitoring and alerting setup
