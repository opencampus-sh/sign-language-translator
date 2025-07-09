# Cloud Infrastructure

This directory contains all cloud infrastructure code for the Sign Language Translation project. The infrastructure is managed using Terraform and organized by environment.

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
└── manage_access.sh            # 🎯 Main access management script

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

## 🔐 Access Management

The `manage_access.sh` script provides comprehensive user access management for both Google Cloud Storage and Vertex AI services.

### Usage

```bash
./manage_access.sh <action> <email> [role] [service]
```

**Actions:** `add`, `remove`, `list`  
**Services:** `storage`, `vertex`, `all`

### Storage Roles

- **`viewer`** - Can only read/download files
- **`writer`** - Can read, write, and upload files
- **`admin`** - Full storage administration access

### Vertex AI Roles

- **`viewer`** - Can view Vertex AI resources
- **`user`** - Can create and manage jobs/models (recommended for processing)
- **`admin`** - Full administrative access
- **`job_user`** - Can run custom jobs only
- **`model_user`** - Can use model endpoints only
- **`endpoint_deployer`** - Can deploy endpoints only

### 🎯 Common Use Cases

#### **Grant Access for Video Processing Pipeline**

For users who need to run the Tagesschau video processing:

```bash
# Grant project viewer access (so they can see the project)
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="user:user@example.com" \
  --role="roles/viewer"

# Grant storage access for uploading CSV and downloading results
./manage_access.sh add user@example.com writer storage

# Grant Vertex AI access for running cloud processing jobs
./manage_access.sh add user@example.com user vertex
```

**What this enables:**

- ✅ See the project in Google Cloud Console
- ✅ Upload CSV files with video links
- ✅ Run `process_tagesschau_videos.ipynb` notebook
- ✅ Monitor job progress in Vertex AI console
- ✅ Download processed landmark and transcript files

#### **Grant Research Access**

For researchers who need to access processed data:

```bash
# Project visibility + read-only storage access
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="user:researcher@university.edu" \
  --role="roles/viewer"

./manage_access.sh add researcher@university.edu viewer storage
```

#### **Grant ML Engineer Access**

For ML engineers who need to train models:

```bash
# Full pipeline access
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="user:ml-engineer@company.com" \
  --role="roles/viewer"

./manage_access.sh add ml-engineer@company.com admin storage
./manage_access.sh add ml-engineer@company.com user vertex
```

### Examples

#### Individual Permissions

```bash
# Add storage writer access
./manage_access.sh add john@company.com writer storage

# Add Vertex AI user access
./manage_access.sh add jane@company.com user vertex

# Add both storage and Vertex AI access
./manage_access.sh add bob@company.com writer all
```

#### Remove Access

```bash
# Remove storage access
./manage_access.sh remove john@company.com writer storage

# Remove Vertex AI access
./manage_access.sh remove jane@company.com user vertex
```

#### List Current Permissions

```bash
# View all current permissions
./manage_access.sh list
```

### 🚨 Important Notes

1. **Project Visibility**: Users need `roles/viewer` at the project level to see the project in their console. This must be granted separately using `gcloud projects add-iam-policy-binding`.

2. **Conditional Policies**: When adding project-level permissions, you may be prompted to specify conditions. Choose option `[2] None` for standard access.

3. **Bucket Availability**: The script automatically skips buckets that don't exist in your environment.

4. **Security**: Always use the minimum required permissions. Start with `viewer` and escalate only when necessary.

### Verification

After granting access, verify permissions with:

```bash
# Check project-level permissions
gcloud projects get-iam-policy YOUR_PROJECT_ID \
  --flatten='bindings[].members' \
  --filter='bindings.members:user@example.com'

# Check storage permissions
gcloud storage buckets get-iam-policy gs://YOUR_BUCKET \
  --flatten='bindings[].members' \
  --filter='bindings.members:user@example.com'
```

For more details about the infrastructure and available resources, see the terraform configurations in `terraform/` directory.
