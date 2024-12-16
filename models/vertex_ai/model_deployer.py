from typing import Optional, Dict, Any
import subprocess
from pathlib import Path
import json

class ModelDeployer:
    def __init__(self, project_id: str, environment: str, region: str = "europe-west3"):
        self.project_id = project_id
        self.environment = environment
        self.region = region


    def trigger_deployment(
        self,
        model_id: str,
        hf_task: str,
        model_version: str = "v1",
        branch: str = "main",
        hf_token: Optional[str] = None,
        trigger_name: Optional[str] = None,
        wait_for_completion: bool = True,
        timeout_minutes: int = 30
    ) -> Dict[str, Any]:
        """
        Trigger a Cloud Build deployment for a Hugging Face model
        
        Args:
            model_id: Hugging Face model ID (e.g., "openai/whisper-small")
            hf_task: Hugging Face task type (e.g., "automatic-speech-recognition")
            model_version: Version string for the endpoint (default: "v1")
            branch: Git branch to use (default: "main")
            hf_token: Optional Hugging Face token
            trigger_name: Optional trigger name (defaults to {environment}-{model_name}-deploy)
            wait_for_completion: Whether to wait for the deployment to complete
            timeout_minutes: Timeout in minutes for waiting for deployment completion
        """
        model_name = Path(model_id).name
        
        endpoint_id = f"{self.environment}-{model_id}-{model_version}".lower()
        
        if trigger_name is None:
            trigger_name = f"{self.environment}-deploy"

        # Build all required substitutions
        substitutions = {
            "_MODEL_ID": model_id,
            "_HF_TASK": hf_task,
            "_REGION": self.region,
            "_ENVIRONMENT": self.environment,
            "_ENDPOINT": endpoint_id
        }
        
        if hf_token:
            substitutions["_HF_TOKEN"] = hf_token
        
        # Convert substitutions dict to string format required by gcloud
        substitutions_str = ",".join(f"{k}={v}" for k, v in substitutions.items())
        
        cmd = [
            "gcloud", "builds", "triggers", "run", trigger_name,
            f"--project={self.project_id}",
            f"--region={self.region}",
            f"--branch={branch}",
            f"--format=json",
            f"--substitutions={substitutions_str}"
        ]
        
        try:
            # First run the command to get the build ID
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            build_info = json.loads(result.stdout)
            build_id = build_info.get('metadata', {}).get('build', {}).get('id')
            
            print(f"Deployment started with build ID: {build_id}")
            
            if wait_for_completion:
                try:
                    # Wait for build completion
                    # ... existing waiting code ...
                    return build_info
                except KeyboardInterrupt:
                    print(f"\nDeployment interrupted. Build ID: {build_id}")
                    print("You can cancel this build using:")
                    print(f"gcloud builds cancel {build_id} --region={self.region}")
                    sys.exit(1)
                    
            return build_info
            
        except subprocess.CalledProcessError as e:
            print(f"Error triggering deployment: {e}")
            print(f"Error output: {e.stderr}")
            raise

    def cancel_deployment(self, build_id: str) -> None:
        """Cancel a running Cloud Build deployment"""
        cmd = [
            "gcloud", "builds", "cancel", build_id,
            f"--region={self.region}",
            f"--project={self.project_id}"
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"Successfully cancelled build {build_id}")
        except subprocess.CalledProcessError as e:
            print(f"Error cancelling build: {e.stderr}")
            raise