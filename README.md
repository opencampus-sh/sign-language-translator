# ML Development Guide

## Overview

This guide explains how to manage training data and models using Google Cloud Storage (GCS) for our sign language translation project.

## Data Storage Structure

```
sign-lang-training-data-dev/
├── raw-videos/         # Original sign language videos
├── processed-frames/   # Extracted and processed frames
├── annotations/        # Labels and annotations
└── datasets/          # Prepared training/validation sets

```

## Prerequisites

1. Install the Google Cloud SDK
2. Have appropriate GCP project permissions
3. Python 3.7+ with required packages:
   ```bash
   pip install google-cloud-storage requests
   ```

## Initial Setup

1. Authenticate and set up your Google Cloud environment:

   ```bash
   # Login to Google Cloud
   gcloud auth login

   # Set your project
   gcloud config set project sign-lang-translator-20241029

   # Verify authentication for Python SDK
   gcloud auth application-default login
   ```

2. Configure your environment:
   ```python
   # config.py
   BUCKET_NAMES = {
       'training': 'sign-lang-training-data-dev',
   }
   ```

## Data Management

### Python Interface

```python
from google.cloud import storage
import requests
import os

def save_training_data_from_remote(remote_url, destination_path):
    """
    Save training data from a remote server to GCS.

    Args:
        remote_url (str): URL of the data on remote server
        destination_path (str): Path in GCS bucket where data should be stored

    Raises:
        requests.exceptions.RequestException: If remote download fails
        google.cloud.exceptions.GoogleCloudError: If GCS upload fails
    """
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAMES['training'])

    # Download from remote server
    response = requests.get(remote_url, stream=True)
    response.raise_for_status()

    # Upload directly to GCS
    blob = bucket.blob(destination_path)
    blob.upload_from_file(response.raw)
    print(f"Successfully uploaded to: gs://{BUCKET_NAMES['training']}/{destination_path}")

def save_local_training_data(local_path, destination_path):
    """
    Save local training data to GCS.

    Args:
        local_path (str): Path to local file
        destination_path (str): Path in GCS bucket
    """
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAMES['training'])
    blob = bucket.blob(destination_path)
    blob.upload_from_filename(local_path)
    print(f"Successfully uploaded to: gs://{BUCKET_NAMES['training']}/{destination_path}")

def load_training_data(destination_path, download_locally=False):
    """
    Load training data from GCS.

    Args:
        destination_path (str): Path in GCS bucket
        download_locally (bool): If True, downloads to local file

    Returns:
        Union[bytes, str]: Either the file contents or local file path
    """
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAMES['training'])
    blob = bucket.blob(destination_path)

    if download_locally:
        local_path = f'/tmp/{os.path.basename(destination_path)}'
        blob.download_to_filename(local_path)
        return local_path

    return blob.download_as_bytes()
```

### Usage Examples

```python
# Save data from remote server
save_training_data_from_remote(
    'https://remote-server.com/dataset.pkl',
    'datasets/training/dataset.pkl'
)

# Save local data
save_local_training_data(
    'path/to/local/dataset.pkl',
    'datasets/training/dataset.pkl'
)

# Load data (in memory)
training_data = load_training_data('datasets/training/dataset.pkl')

# Load data (to local file)
local_file_path = load_training_data('datasets/training/dataset.pkl', download_locally=True)
```

### Command Line Operations

```bash
# Download from remote server and upload to GCS
curl -L "https://remote-server.com/dataset.pkl" | \
    gsutil cp - gs://sign-lang-training-data-dev/datasets/training/dataset.pkl

# Alternative using wget
wget -qO- "https://remote-server.com/dataset.pkl" | \
    gsutil cp - gs://sign-lang-training-data-dev/datasets/training/dataset.pkl

# Upload local files
gsutil cp ./local_dataset.pkl gs://sign-lang-training-data-dev/datasets/training/dataset.pkl

# Upload multiple files (parallel)
gsutil -m cp -r ./datasets/*.pkl gs://sign-lang-training-data-dev/datasets/training/

# Download from GCS
gsutil cp gs://sign-lang-training-data-dev/datasets/training/dataset.pkl ./local_dataset.pkl

# Download directory (parallel)
gsutil -m cp -r gs://sign-lang-training-data-dev/datasets/training/* ./local_datasets/
```

### Useful Commands

```bash
# List available datasets
gsutil ls gs://sign-lang-training-data-dev/datasets/training/

# Check file size
gsutil du -h gs://sign-lang-training-data-dev/datasets/training/dataset.pkl

# Add metadata to uploads
gsutil -h "Content-Type:application/octet-stream" \
    cp ./dataset.pkl gs://sign-lang-training-data-dev/datasets/training/

# Check file metadata
gsutil stat gs://sign-lang-training-data-dev/datasets/training/dataset.pkl
```

## Best Practices

1. **Performance**

   - Use the `-m` flag for parallel operations with multiple or large files
   - Stream large files directly instead of loading them into memory
   - Consider using `gsutil -o GSUtil:parallel_composite_upload_threshold=150M` for large files

2. **Organization**

   - Follow the established bucket structure
   - Use clear, consistent naming conventions
   - Add appropriate metadata to uploaded files

3. **Security**

   - Never commit credentials
   - Use appropriate IAM roles
   - Regularly rotate service account keys

## Troubleshooting

Common issues and solutions:

- Permission denied: Verify your authentication and IAM roles
- Timeout errors: Consider using resumable uploads for large files
- Rate limiting: Implement exponential backoff in your code

## Support

For additional help:

- Check [GCS Documentation](https://cloud.google.com/storage/docs)
