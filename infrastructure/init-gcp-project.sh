#!/bin/bash
# Script to initialize Google Cloud Project for Sign Language Translation ML
# Usage: ./init-gcp-project.sh ORGANIZATION_ID BILLING_ACCOUNT_ID FOLDER_ID

if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
    echo "Please provide organization ID, billing account ID, and folder ID"
    echo "Usage: ./init-gcp-project.sh ORGANIZATION_ID BILLING_ACCOUNT_ID FOLDER_ID"
    exit 1
fi

ORGANIZATION_ID=$1
BILLING_ACCOUNT_ID=$2
FOLDER_ID=$3
TIMESTAMP=$(date +%Y%m%d)
PROJECT_ID="sign-lang-translator-$TIMESTAMP"

echo "Creating project with ID: $PROJECT_ID in folder: $FOLDER_ID"

# Create project under the specified folder
gcloud projects create $PROJECT_ID \
    --folder=$FOLDER_ID \
    --name="Sign Language Translation ML"

# Link billing account
gcloud billing projects link $PROJECT_ID \
    --billing-account=$BILLING_ACCOUNT_ID

# Set as active project
gcloud config set project $PROJECT_ID

# Set region and zone to Frankfurt
gcloud config set compute/region europe-west3
gcloud config set compute/zone europe-west3-a

echo "Project setup complete in folder $FOLDER_ID"
echo "Project ID: $PROJECT_ID"
echo "Please verify settings with: gcloud config list"
