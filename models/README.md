# Model Management

This directory contains model-related code and utilities for the Sign Language Translator project. It includes model definitions, training scripts, and deployment configurations.

## Directory Structure

models/
├── types/ # Model type implementations
│ ├── huggingface/ # Hugging Face model deployment
│ └── mock/ # Mock model for testing
├── vertex_ai/ # Vertex AI integration
└── build_model_experimentation_lineage_with_prebuild_code.ipynb # Batch processing example

## Getting Started with Batch Processing

The `build_model_experimentation_lineage_with_prebuild_code.ipynb` notebook demonstrates how to process data in batch using Vertex AI. Before running the notebook, ensure proper access is configured.

### 1. Access Requirements

Users need specific permissions for both Cloud Storage and Vertex AI. An administrator must grant these using the `manage_access.sh` script:

```bash
# Grant storage access
./infrastructure/manage_access.sh add user@example.com writer storage

# Grant Vertex AI access
./infrastructure/manage_access.sh add user@example.com writer vertex

# Or grant both at once
./infrastructure/manage_access.sh add user@example.com writer all
```

Available roles:

- `viewer`: Read-only access
- `writer`: Read and write access
- `admin`: Full access including management operations

### 2. Storage Bucket Structure

The project uses five distinct buckets, each with a specific purpose:

1. Raw Data Bucket (`${PROJECT_ID}-${ENV}-raw-data`):

   - Stores the initial CSV files with video links
   - Source data for the preprocessing pipeline

2. Landmarks Data Bucket (`${PROJECT_ID}-${ENV}-landmarks`):

   - Stores the extracted MediaPipe landmarks
   - Output from the preprocessing pipeline

3. Training Data Bucket (`${PROJECT_ID}-${ENV}-training`):

   - Stores processed features ready for model training
   - Input for training pipelines

4. Models Bucket (`${PROJECT_ID}-${ENV}-models`):

   - Stores trained model artifacts and checkpoints
   - Longer retention period (90 days)

5. Staging Bucket (`${PROJECT_ID}-${ENV}-staging`):
   - Temporary storage for Vertex AI jobs
   - Automatically cleaned up after 1 day

Example bucket names for development environment:

```
sign-lang-translator-20241029-dev-raw-data
sign-lang-translator-20241029-dev-landmarks
sign-lang-translator-20241029-dev-training
sign-lang-translator-20241029-dev-models
sign-lang-translator-20241029-dev-staging
```

Data Flow:

1. Raw videos/CSV → `raw-data` bucket
2. MediaPipe processing → `landmarks` bucket
3. Feature extraction → `training` bucket
4. Model training → `models` bucket
5. Vertex AI jobs use → `staging` bucket

### 3. Running the Batch Processing Job

The batch processing notebook (`batch_processing.ipynb`) demonstrates how to process videos using MediaPipe in parallel on Vertex AI. Here's how to use it:

1. **Environment Setup**

   - Open the notebook in Vertex AI Workbench or locally
   - Ensure you have the necessary permissions (see Section 1)
   - The notebook will automatically detect the project root and load configurations

2. **Configure Processing** ```python

   # Example configuration

   job_config = JobConfig(
   provisioning_model="SPOT", # Use spot instances for cost savings
   restart_on_failure=True, # Auto-restart failed jobs
   timeout_days=1 # Maximum runtime
   )

   machine_config = MachineConfig(
   machine_type="n1-standard-4",
   accelerator_type=None, # CPU-only for MediaPipe
   disk_size_gb=100
   ) ```

3. **Submit the Job** ```python
   processor = CloudProcessor(
   project_id=config['project_id'],
   location=config['region'],
   staging_bucket=f"{config['project_id']}-{config['environment']}-staging"
   )

   job = processor.submit_job(
   processing_fn=processing_function,
   input_bucket=f"{config['project_id']}-{config['environment']}-raw-data",
   output_bucket=f"{config['project_id']}-{config['environment']}-landmarks",
   workers=10, # Number of parallel workers
   machine_config=machine_config,
   job_config=job_config,
   batch_size=10 # Videos per batch
   ) ```

4. **Monitor Progress**

   - View job status in the Vertex AI Console:
     - Go to Vertex AI > Training > Training jobs
     - Find your job by name (format: "video-process")
     - Monitor logs and resource usage

5. **Results**

   - Processed landmarks will be saved to the landmarks bucket
   - Each file will be prefixed with "processed\_"
   - Failed jobs will automatically restart if configured

6. **Cost Optimization**

   - Uses spot instances by default (70% cheaper)
   - Automatic cleanup of staging data after 1 day
   - Parallel processing reduces total runtime

7. **Common Issues**
   - If job fails with permission errors, verify bucket access
   - For timeout errors, increase `timeout_days` in JobConfig
   - For memory issues, reduce `batch_size` or increase `machine_type`
