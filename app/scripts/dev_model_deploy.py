import os
import argparse
from google.cloud import aiplatform
from google.cloud import storage

def setup_dev_endpoint(
    project_id: str,
    location: str,
    model_display_name: str,
    container_image_uri: str = "europe-docker.pkg.dev/vertex-ai/prediction/pytorch-cpu.1-13:latest"
):
    """
    Sets up a lightweight development endpoint on Vertex AI
    """
    aiplatform.init(project=project_id, location=location)

    # Use a CPU-only container and minimal compute resources
    endpoint = aiplatform.Endpoint.create(
        display_name=f"dev-{model_display_name}"
    )

    model = aiplatform.Model.upload(
        display_name=model_display_name,
        artifact_uri=f"gs://{project_id}-model-artifacts/dev-latest/",
        serving_container_image_uri=container_image_uri,
        serving_container_environment_variables={
            "MODEL_PATH": "dev-latest",
            "USE_CPU": "true",
            "MAX_BATCH_SIZE": "1"  # Limit batch size for dev
        },
        serving_container_resources={
            "cpu_limit": "2",
            "memory_limit": "4G"
        }
    )

    model.deploy(
        endpoint=endpoint,
        machine_type="n1-standard-2",
        min_replica_count=1,
        max_replica_count=1,
        sync=True
    )

    return endpoint

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Deploy model to development endpoint')
    parser.add_argument('--project-id', required=True, help='GCP Project ID')
    parser.add_argument('--location', default='europe-west3', help='GCP Region')
    parser.add_argument('--model-name', default='sign-language-translator-dev', 
                       help='Model display name')
    
    args = parser.parse_args()
    endpoint = setup_dev_endpoint(args.project_id, args.location, args.model_name)
    print(f"Development endpoint created: {endpoint.resource_name}") 