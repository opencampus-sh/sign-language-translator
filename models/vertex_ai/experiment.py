from dataclasses import dataclass
from typing import Optional, Dict, Any
import os
from pathlib import Path
import yaml
from google.cloud import aiplatform

@dataclass
class ExperimentConfig:
    """Configuration for model experimentation"""
    project_id: str
    region: str = "europe-west3"
    machine_type: str = "n1-standard-4"
    accelerator_type: Optional[str] = "NVIDIA_TESLA_T4"
    accelerator_count: int = 1
    bucket_name: Optional[str] = None

    @classmethod
    def from_yaml(cls, environment: str = "dev") -> "ExperimentConfig":
        """Load configuration from existing YAML files"""
        config_path = Path(__file__).parent / "config" / f"{environment}.yaml"
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found at {config_path}")
            
        with open(config_path) as f:
            config = yaml.safe_load(f)
        
        # Get project configuration
        project_config = config.get("project", {})
        project_id = project_config.get("project_id")
        
        if not project_id:
            # Fallback to environment variable
            project_id = os.getenv("GCP_PROJECT_ID")
            if not project_id:
                raise ValueError("Project ID not found in config or environment variables")
        
        # Construct bucket name from project ID if not specified
        vertex_config = config.get("vertex_ai", {})
        bucket_name = vertex_config.get("artifacts_bucket")
        if not bucket_name:
            bucket_name = f"{project_id}-{environment}-vertex-ai-artifacts"
        
        return cls(
            project_id=project_id,
            region=project_config.get("region", "europe-west3"),
            bucket_name=bucket_name,
            machine_type=vertex_config.get("machine_type", "n1-standard-4"),
            accelerator_type=vertex_config.get("accelerator_type", "NVIDIA_TESLA_T4"),
            accelerator_count=vertex_config.get("accelerator_count", 1)
        )

class VertexAIExperiment:
    """Simplified interface for preprocessing and training on Vertex AI"""
    
    def __init__(self, config: Optional[ExperimentConfig] = None, environment: str = "dev"):
        self.config = config or ExperimentConfig.from_yaml(environment)
        self.environment = environment
        
        # Initialize Vertex AI
        aiplatform.init(
            project=self.config.project_id,
            location=self.config.region
        )
    
    def submit_preprocessing_job(
        self, 
        script_path: str, 
        args: Optional[Dict[str, Any]] = None,
        sync: bool = True
    ) -> aiplatform.CustomJob:
        """Submit a preprocessing job to Vertex AI"""
        
        # Ensure script exists
        if not Path(script_path).exists():
            raise FileNotFoundError(f"Script not found at {script_path}")
            
        job = aiplatform.CustomJob.from_local_script(
            display_name=f"preprocessing-job-{self.environment}",
            script_path=script_path,
            container_uri="us-docker.pkg.dev/vertex-ai/training/pytorch-gpu.1-13:latest",
            args=args or {},
            requirements=["google-cloud-storage", "pandas", "numpy"],
            machine_type=self.config.machine_type,
            accelerator_type=self.config.accelerator_type,
            accelerator_count=self.config.accelerator_count
        )
        
        job.run(sync=sync)
        return job
    
    def submit_training_job(
        self, 
        script_path: str, 
        args: Optional[Dict[str, Any]] = None,
        sync: bool = True
    ) -> aiplatform.CustomJob:
        """Submit a training job to Vertex AI"""
        
        # Ensure script exists
        if not Path(script_path).exists():
            raise FileNotFoundError(f"Script not found at {script_path}")
            
        job = aiplatform.CustomJob.from_local_script(
            display_name=f"training-job-{self.environment}",
            script_path=script_path,
            container_uri="us-docker.pkg.dev/vertex-ai/training/pytorch-gpu.1-13:latest",
            args=args or {},
            requirements=["torch", "transformers", "datasets", "evaluate"],
            machine_type=self.config.machine_type,
            accelerator_type=self.config.accelerator_type,
            accelerator_count=self.config.accelerator_count
        )
        
        job.run(sync=sync)
        return job 