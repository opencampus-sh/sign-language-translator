# Google Cloud Project Setup Guide

This guide explains how to set up your Google Cloud Project for the Sign Language Translation service.

## Prerequisites

1. [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed
2. Access to the OpenCampus organization in Google Cloud
3. Required information:
   - Organization ID
   - Billing Account ID
   - ML Projects Folder ID

## Initial Setup

1. Get your organization ID:

```bash
gcloud organizations list
```

2. Get you billing account ID:

```bash
gcloud beta billing accounts list
```

3. Get your ML Projects folder ID:

```bash
gcloud resource-manager folders list --organization=YOUR_ORGANIZATION_ID
```

4. Run the setup script:

```bash
./setup/init-gcp-project.sh YOUR_ORGANIZATION_ID YOUR_BILLING_ACCOUNT_ID YOUR_FOLDER_ID
```

## What Gets Set Up

The initialization script will:

- Create a new project under your organization
- Link it to the specified billing account
- Enable required APIs:
  - Compute Engine
  - Cloud Storage
  - Cloud Resource Manager
- Set default region to Frankfurt (europe-west3)

## Verification

After setup, verify your configuration:

```bash
gcloud config list
```

Expected output should show:

- Project: sign-lang-translator-[DATE]
- Region: europe-west3
- Zone: europe-west3-a

## Managing Access

Use the provided access management script to control bucket permissions:

1. Grant access:

```bash
./setup/manage_access.sh add employee@company.com viewer
./setup/manage_access.sh add employee@company.com writer
```

2. Remove access:

```bash
./setup/manage_access.sh remove employee@company.com viewer
```

3. List current permissions:

```bash
./setup/manage_access.sh list
```

## Troubleshooting

If you see permission errors, verify your roles:

```bash
gcloud projects get-iam-policy YOUR_PROJECT_ID
```

Common issues:

- "Permission denied": Ensure you have Organization Admin role
- "Billing account not found": Verify billing account ID and permissions
- "Folder not found": Check folder ID and organization permissions

## Next Steps

After successful project setup:

1. [Configure your development environment](DEPLOYMENT.md)
2. [Set up infrastructure with Terraform](../terraform/environments/README.md)
