# Unsere große Vision
Wir möchten mehr als nur Sprachbarrieren überwinden. Wir möchten das Menschen mit unserer Technologie so angenehm wie möglich miteinander kommunizieren. Als Open-Source Projekt geht es uns darum gemeinnützig eine Software zu entwickeln, die als Schnittstelle zwischen Gehörlosen und Hörenden dient. Sofern möglich, streben wir deshalb an, Gebärden in Echtzeit zu verbalisieren und gleichzeitig das gesprochene des Gesprächspartners wieder mit animierten gebärdenden Avataren zu übersetzen, die durch eine AR-Brille ins Sichtfeld der Gehörlosen Person prohiziert werden. So soll es möglich werden, dass Menschen in Ihrer bevorzugten Sprache mit einander kommunizieren, während unsere KI die Brücke zwischen den Sprachen baut.

https://github.com/user-attachments/assets/25741ed1-ce6a-42b3-a297-1f8de950f741

# Unsere Vision für den ersten Prototypen Ende Januar 2025
Um unserer großen Vision einen Schritt näher zu kommen, planen wir für Ende Januar 2025 eine erste KI zu trainieren, die die Gebärden mit so geringer Verzögerung wie möglich transkribiert und verbalisiert. Diese KI soll zunächst in einer Web-APP integriert werden. Diese App sollen Nutzer über unsere kommende Internetseite aufrufen können. Dort werden Sie zunächst darum gebeten Ihre Kamera freizugeben, damit unsere KI Ihre Gebärden analysieren und transkribieren kann. Die transkribierten Gebärden werden dann auch durch Text-to-Speech Software verbalisiert und über die Lautsprecher ihres Notebooks wiedergegeben damit andere Personen Ihre Gebärden hören können. Auf das gehörte kann dann geantwortet werden und Sie sehen was gesagt wird durch die Implementierung einer Speech-to-Text KI. So soll unsere Web-APP zunächst ermöglichen, dass Gebärden und Gesprochenes als Textnachrichten in einem Chat Fenster automatisch protokolliert und für die hörende Person zusätzlich vorgelesen werden. 

https://github.com/user-attachments/assets/37a38a94-b832-4600-ba67-3f1fd02adaae

# Unser Team 
Wir sind Christoph, Emel, Henner, Henrik, Jeremy, Kaan und Steffen.  
Falls dich das Thema begeistert, dann schreibe uns gerne eine Nachricht. 
Wir freuen uns immer über Verstärkung. Zurzeit freuen wir uns am meisten über Personen, die uns unterstüzen bei
- Datenvorverarbeitung 
- Programmieren 
- Testen
- Evaluieren

# Unser Vorgehen
Damit wir schaffen, was wir uns vorgenommen haben arbeiten wir strukturiert. Wir treffen uns wöchentlich und verfolgen einen konkreten Projektplan.
Technisch unterteilt sich unsere Arbeit in die:
- Vorverarbeitung von Videos mit Gebärdendolmetschern
- Training des KI Modells Whisper Large
- Entwickeln der Nutzeroberfläche
- Bereitstellung und Einbindung der KI-komponenten 

![Architektur](https://github.com/user-attachments/assets/2851d597-3c30-4470-becf-4284fbbecd98)


# Sign Language Translator

This project provides a sign language translation service using MediaPipe for keypoint extraction and a fine-tuned Whisper model deployed on Vertex AI. The service is deployed on Google Cloud Run and managed with Terraform.

## Project Structure

```
sign-language-translator/
├── app/ # Application code
│ ├── config/ # Configuration files
│ ├── data/ # Data files
│ ├── models/ # Model implementations
│ └── utils/ # Helper functions
└── infrastructure/ # Deployment code
  ├── terraform/ # Infrastructure as Code
  │ ├── environments/ # Environment-specific configs
  │ └── modules/ # Reusable Terraform modules
  └── cloud-build/ # Cloud Build configurations


sign-language-translator/
├── app/                            # Your application code
│   ├── config/                     # Application configuration
│   ├── data/                       # Application data
│   └── scripts/                    # Application-specific scripts
├── infrastructure/                 # Infrastructure as code
│   └── terraform/
│       ├── environments/
│       │   └── dev/
│       │       └── main.tf         # Environment configuration
│       ├── modules/
│       │   ├── monitoring/         # Monitoring module
│       │   └── vertex_ai/          # Vertex AI module
│       │       ├── main.tf         # Core Vertex AI resources
│       │       ├── variables.tf    # Module variables
│       │       └── outputs.tf      # Module outputs
│       └── terraform.tfvars
├── models/                         # ML models as a top-level concern
│   └── huggingface_model/          # Specific model implementation
│       ├── cloudbuild/             # Cloud Build configurations for
│       │   └── cloudbuild.yaml     #    automatic deployment to staging and
│       ├── docker/
│       │   ├── Dockerfile         # Prediction routine container
│       │   ├── predictor.py       # Prediction code
│       │   └── requirements.txt   # Model dependencies
│       ├── scripts/               # For manual deployment in development environment
│       │   ├── build_and_push.py  # Docker image management
│       │   ├── download_model.py  # Model preparation
│       │   └── deploy_model.py    # Model deployment
│       └── README.md              # Model-specific documentation
└── README.md
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
# Make the setup script executable
chmod +x setup/setup_dev_env.sh
# Run the development setup script
./setup/setup_dev_env.sh
```

2. Configure your environment:

```bash
# For offline development (using mock model)
export USE_MOCK_MODEL=true

# For online development (using Vertex AI)
export USE_MOCK_MODEL=false
export VERTEX_AI_ENDPOINT_ID=<endpoint-id-from-previous-step>
```

If you want to have access to a Vertex AI endpoint to contribute to the project, contact the project maintainers.

3. Start the development app:

```bash
python app/main.py
```

You can find an example ASL video in the repository at [app/data/samples/asl_example.mp4](https://github.com/opencampus-sh/sign-language-translator/blob/main/app/data/samples/asl_example.mp4). This example video is sourced from [Pexels](https://www.pexels.com/search/videos/sign%20language/), a free stock video platform.

## VS Code Setup

1. Install recommended extensions when prompted by VS Code
2. Sign in to GitHub when prompted by the GitHub Pull Requests and Issues extension
3. Workspace settings will automatically configure:
   - Standardized branch naming for issues
   - GitHub issue integration
   - Pull request management

## Contributing

1. Create a fork of the repository

2. Create a feature branch:

```bash
git checkout -b feature/your-feature-name
```

3. Make your changes and test:

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

- Create an issue [here](https://github.com/opencampus-sh/sign-language-translator/issues)
