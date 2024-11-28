# Cloud Infrastructure

This directory contains all cloud infrastructure code for the Sign Language Translation project. The infrastructure is managed using Terraform and organized by environment.

## Prerequisites

1. [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed
2. Access to the OpenCampus organization in Google Cloud
3. Appropriate permissions:
   - Organization viewer
   - Project creator
   - Billing account user
4. Email address for monitoring alerts
5. [Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-terraform) installed

## Structure

```
infrastructure/                 # Infrastructure as code
├── terraform/
│   ├── environments/
│   │   └── dev/
│   │       └── main.tf         # Environment configuration
│   ├── modules/
│   │   ├── monitoring/         # Monitoring module
│   │   └── vertex_ai/          # Vertex AI module
│   │       ├── main.tf         # Core Vertex AI resources
│   │       ├── variables.tf    # Module variables
│   │       └── outputs.tf      # Module outputs
│   └── terraform.tfvars
├── README.md
├── init-gcp-project.sh
├── setup_dev_env.sh
└── manage_access.sh

```

## Initial Setup for the Google Cloud Project

1. Get your organization ID:
   ```bash
   gcloud organizations list
   ```
2. Get your billing account ID:
   ```bash
   gcloud billing accounts list
   ```
3. Get the ML Projects folder ID:
   ```bash
   gcloud resource-manager folders list --organization=YOUR_ORGANIZATION_ID
   ```
4. Run the setup script:
   ```bash
   ./setup/init-gcp-project.sh YOUR_ORGANIZATION_ID YOUR_BILLING_ACCOUNT_ID YOUR_FOLDER_ID
   ```

### What Gets Set Up

- New project created under the given organization
- Project linked to billing account
- Default region set to Frankfurt (europe-west3)

## Infrastructure Setup

### Environment Setup

This project uses Terraform variables for configuration. For local development:

1. Copy the example variables file:

   ```bash
   cd terraform/environments/dev
   cp example.tfvars terraform.tfvars
   ```

2. Edit terraform.tfvars with your values:
   ```hcl
   project_id = "your-project-id"
   region     = "europe-west3"
   ```

### Infrastructure Components

- Storage Buckets:

  - Training data storage
  - (Model artifacts storage)
  - (Evaluation results storage)

- IAM Configuration:

  - Role-based access control
  - (Service accounts for automation)

- Vertex AI:

  - Endpoint

- Monitoring and Alerting:

  - Cloud Logging
  - Cloud Error Reporting
  - Cloud Billing Budget

## Environment Management

- Development: Used for active development and testing

  - Less restricted access
  - Development-sized resources

- Staging: Used for training and serving models
  - Stricter access controls
  - Near production-grade resources

## Useful Commands

```bash
# Check infrastructure status
terraform plan

# Apply changes
terraform apply

# Destroy resources (careful!)
terraform destroy

# Format terraform files
terraform fmt
```

## Access Management

### Adding New Team Members

We provide a script to easily manage user access to GCS buckets. The script is located in `setup/manage_access.sh`.

1. Grant access:

```bash
./manage_access.sh add employee@company.com viewer
./manage_access.sh add employee@company.com writer
```

2. Remove access:

```bash
./manage_access.sh remove employee@company.com viewer
```

3. List current permissions:

```bash
./manage_access.sh list
```

For more details about the infrastructure and available resources, see the terraform configurations in `terraform/` directory.
