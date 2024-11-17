# Sign Language Translator

This project provides a sign language translation service using MediaPipe for keypoint extraction and a fine-tuned Whisper model deployed on Vertex AI. The service is deployed on Google Cloud Run and managed with Terraform.

## Documentation

- [Data Access and Dataset Information](app/docs/DATA.md)
- [Model Training Guide](app/docs/TRAINING.md)
- [Deployment Scenarios](app/docs/DEPLOYMENT.md)
- [GCP Project Setup Guide](app/docs/GCP_SETUP.md)

## Project Structure

```
sign-language-translator/
├── app/ # Application code
│ ├── config/ # Configuration files
│ ├── models/ # Model implementations
│ ├── scripts/ # Utility scripts
│ └── utils/ # Helper functions
├── terraform/ # Infrastructure as Code
│ ├── environments/ # Environment-specific configs
│ └── modules/ # Reusable Terraform modules
├── cloud-build/ # Cloud Build configurations
└── setup/ # Setup scripts
```

## Prerequisites

- Python 3.9+
  - Specific version requirements listed in requirements.txt
- Google Cloud SDK
  - Required permissions:
    - Organization viewer
    - Project creator
    - Billing account user
    - Service Account Admin
- Terraform >= 1.0.0
- Docker (optional for local container testing)
- Hugging Face account and access token (for production model)

For Linux users:

```bash
sudo apt-get update
sudo apt-get install python3-dev build-essential
```

## Environment Variables

Required environment variables:

- `PROJECT_ID`: Your Google Cloud project ID
- `REGION`: Default GCP region (e.g., europe-west3)
- `GITHUB_OWNER`: GitHub username or organization name
- `NOTIFICATION_EMAIL`: Email for monitoring alerts
- `USE_MOCK_MODEL`: Set to "true" for offline development
- `VERTEX_AI_ENDPOINT_ID`: Required when USE_MOCK_MODEL is "false"

## Development Setup

1. Initialize your development environment:

```bash
# Clone the repository
git clone https://github.com/your-org/sign-language-translator.git
cd sign-language-translator
# Run the development setup script
./setup/setup_dev_env.sh
```

2. Configure your environment:

```bash
# For offline development (using mock model)
export USE_MOCK_MODEL=true
# For online development (using Vertex AI)
export USE_MOCK_MODEL=false
export VERTEX_AI_ENDPOINT_ID=<your-endpoint-id>
```

3. Deploy a development model (if using Vertex AI):

```bash
python app/scripts/dev_model_deploy.py --project-id=your-project-id
```

4. Start the development server:

```bash
flask run --debug
```

## Deployment Scenarios

### Development

- Uses CPU-only resources
- Single replica deployment
- Mock model available for offline development
- Minimal compute resources for cost optimization

### Staging

- GPU-enabled endpoints
- Automated deployment via GitHub Actions
- Integration testing before promotion
- Scaled-down production configuration

### Production

- Full GPU resources
- Multiple replicas for high availability
- Automated canary deployments
- Full monitoring and alerting

## Model Deployment

### Development

```bash
# Deploy development model
python app/scripts/dev_model_deploy.py --project-id=your-project-id
```

### Staging/Production

```bash
# Tag a new model version
git tag model/v1.0.0
git push origin model/v1.0.0
# GitHub Actions will automatically:
# 1. Deploy to staging
# 2. Run validation tests
# 3. Deploy to production if tests pass
```

## Infrastructure Setup

1. Copy the example variables file:

```bash
cd terraform/environments/dev
cp example.tfvars terraform.tfvars
```

2. Edit terraform.tfvars with your values

```hcl
project_id = "your-project-id"
region = "europe-west3"
```

3. Initialize and apply Terraform:

```bash
terraform init
terraform apply
```

## Monitoring Setup

The project includes monitoring configurations for different environments:

### Development

- Basic resource monitoring
- Error rate tracking
- Performance metrics

### Production

- Full monitoring suite
- Custom alerts
- Uptime checks
- Error tracking
- Performance monitoring

Configure monitoring by setting up notification channels:

```bash
cd terraform/environments/[env]
terraform apply -var="notification_email=your-email@domain.com"
```

## Troubleshooting

Common issues and solutions:

1. **Permission Issues**

   - Verify your GCP credentials are properly set up
   - Ensure you have the required IAM roles
   - Check project permissions

2. **Deployment Failures**

   - Verify your terraform.tfvars configuration
   - Check Cloud Build logs
   - Ensure service account has necessary permissions

3. **Model Issues**
   - For mock model: Verify USE_MOCK_MODEL=true
   - For Vertex AI: Check endpoint ID and permissions

## Contributing

1. Create a feature branch:

```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and test:

```bash
# Run tests
pytest
# Format code
black app/
# Check linting
flake8 app/
```

3. Submit a pull request

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Support

For support and questions:

- Create an issue in the GitHub repository
