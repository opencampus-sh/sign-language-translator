from dataclasses import dataclass
from typing import Optional, Dict, Any, List, Union
from pathlib import Path
from google.cloud import aiplatform

@dataclass
class TrainingConfig:
    """Configuration for model training"""
    project_id: str
    region: str = "europe-west3"
    machine_type: str = "n1-standard-4"
    accelerator_type: Optional[str] = "NVIDIA_TESLA_T4"
    accelerator_count: int = 1
    data_bucket: Optional[str] = None

    @classmethod
    def from_yaml(cls, environment: str = "dev") -> "TrainingConfig":
        """Load configuration from existing YAML files"""
        # ... existing config loading code ...

class ModelTrainer:
    """Manages model training and experimentation on Vertex AI"""
    
    def __init__(
        self, 
        config: Optional[TrainingConfig] = None, 
        environment: str = "dev",
        data_bucket: Optional[str] = None
    ):
        self.config = config or TrainingConfig.from_yaml(environment)
        self.environment = environment
        
        # Override config bucket if provided
        if data_bucket:
            self.config.data_bucket = data_bucket.replace('gs://', '')
        
        # Initialize Vertex AI
        aiplatform.init(
            project=self.config.project_id,
            location=self.config.region
        )
        
    def create_experiment(
        self, 
        experiment_name: str,
        description: Optional[str] = None
    ) -> aiplatform.Experiment:
        """Create a new experiment for tracking multiple training runs"""
        return aiplatform.Experiment.create(
            display_name=experiment_name,
            description=description
        )
    
    def start_run(
        self,
        experiment_name: str,
        run_name: str,
        params: Optional[Dict[str, Any]] = None
    ) -> aiplatform.ExperimentRun:
        """Start a new experimental run within an experiment"""
        experiment = aiplatform.Experiment(experiment_name)
        return experiment.start_run(
            run=run_name,
            parameters=params or {}
        )
    
    def submit_hyperparameter_tuning_job(
        self,
        script_path: str,
        metric_id: str,
        parameter_specs: Dict[str, Dict[str, Union[float, int, str]]],
        max_trials: int = 10,
        parallel_trials: int = 3,
        args: Optional[Dict[str, Any]] = None
    ) -> aiplatform.HyperparameterTuningJob:
        """Submit a hyperparameter tuning job"""
        # Ensure script exists
        if not Path(script_path).exists():
            raise FileNotFoundError(f"Script not found at {script_path}")
            
        job = aiplatform.HyperparameterTuningJob(
            display_name=f"hparam-tuning-{self.environment}",
            optimization_metric_id=metric_id,
            parameter_specs=parameter_specs,
            max_trial_count=max_trials,
            parallel_trial_count=parallel_trials,
            custom_job_spec={
                "script_path": script_path,
                "container_uri": "us-docker.pkg.dev/vertex-ai/training/pytorch-gpu.1-13:latest",
                "args": args or {},
                "requirements": ["torch", "transformers", "datasets", "evaluate"],
                "machine_type": self.config.machine_type,
                "accelerator_type": self.config.accelerator_type,
                "accelerator_count": self.config.accelerator_count
            }
        )
        
        job.run()
        return job
    
    def submit_training_job(
        self, 
        script_path: str, 
        args: Optional[Dict[str, Any]] = None,
        experiment_name: Optional[str] = None,
        run_name: Optional[str] = None,
        sync: bool = True
    ) -> aiplatform.CustomJob:
        """Submit a training job to Vertex AI with optional experiment tracking"""
        # Ensure script exists
        if not Path(script_path).exists():
            raise FileNotFoundError(f"Script not found at {script_path}")
        
        # Start experiment run if specified
        run = None
        if experiment_name and run_name:
            run = self.start_run(experiment_name, run_name, args)
            
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
        
        # Log job details to experiment if running
        if run:
            run.log_metrics({
                "job_id": job.resource_name,
                "status": job.state.name
            })
            
        return job
    
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
    