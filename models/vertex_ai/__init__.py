import yaml
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv
import os

def setup_environment() -> None:
    """Load environment variables from .env file at project root"""
    current_path = Path(__file__).parent.parent.parent  # Go up from models/config to project root
    env_path = current_path / '.env'
    
    if env_path.exists():
        load_dotenv(env_path, override=True)
        print("Environment variables loaded from .env")
    else:
        print("Warning: No .env file found at project root")

# Load environment variables when config module is imported
setup_environment()

class ModelConfig:
    """Configuration loader for model deployment settings"""
    
    def __init__(self, environment: str = "dev"):
        """
        Initialize configuration for specified environment
        
        Args:
            environment: Name of the environment (dev, prod, etc.)
        """
        self.environment = environment
        self.config = self._load_config()
        
        # Verify critical environment variables
        self._verify_environment()
    
    def _verify_environment(self) -> None:
        """Verify that critical environment variables are set"""
        required_vars = ['HUGGINGFACE_TOKEN']  # Add other required variables here
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        config_path = Path(__file__).parent / "config" / f"{self.environment}.yaml"
        print(f"Loading configuration from {config_path}")
        if not config_path.exists():
            raise FileNotFoundError(f"No configuration found for environment '{self.environment}'")
            
        with open(config_path) as f:
            return yaml.safe_load(f)
    
    @property
    def project_id(self) -> str:
        """GCP project ID"""
        return self.config["project"]["project_id"]
    
    @property
    def region(self) -> str:
        """GCP region"""
        return self.config["project"]["region"]
    
    @property
    def artifacts_bucket(self) -> str:
        """GCS bucket for model artifacts"""
        return self.config["vertex_ai"]["artifacts_bucket"]
    
    @property
    def artifact_registry(self) -> str:
        """Artifact Registry repository name"""
        return self.config["vertex_ai"]["artifact_registry"]
    
    @property
    def endpoint_name(self) -> str:
        """Vertex AI endpoint name"""
        return self.config["vertex_ai"]["endpoint_name"]
    
    @property
    def model_id(self) -> str:
        """Hugging Face model ID"""
        return self.config["model"]["model_id"]
    
    @property
    def task(self) -> str:
        """Hugging Face task type"""
        return self.config["model"]["task"]
    
    @property
    def version(self) -> str:
        """Model version"""
        return self.config["model"]["version"]

# Convenience function to get configuration
def get_config(environment: str = "dev") -> ModelConfig:
    """
    Get configuration for specified environment
    
    Args:
        environment: Name of the environment (dev, prod, etc.)
    
    Returns:
        ModelConfig instance
    """
    return ModelConfig(environment)

__all__ = ['ModelConfig', 'get_config']