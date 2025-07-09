from google.cloud import aiplatform
from google.cloud import storage
import math
import ast
import re
from dataclasses import dataclass
from typing import Optional, Literal, List
from threading import Thread
from tqdm import tqdm
import time

@dataclass
class MachineConfig:
    machine_type: str = "n1-standard-4"
    accelerator_type: Optional[str] = None
    accelerator_count: int = 0
    disk_size_gb: int = 100

@dataclass
class JobConfig:
    provisioning_model: Literal["DEDICATED", "SPOT"] = "SPOT"
    restart_on_failure: bool = True
    timeout_days: Optional[float] = 2.0

class CloudProcessor:
    def __init__(
        self, 
        project_id: str, 
        location: str = "us-central1", 
        staging_bucket: str = None,
        data_bucket: str = None
    ):
        """Initialize CloudProcessor
        Args:
            project_id (str): GCP project ID
            location (str): GCP region
            staging_bucket (str): Bucket name without gs:// prefix
            data_bucket (str): Main data bucket name without gs:// prefix
        """
        if not staging_bucket:
            raise ValueError("A staging bucket must be provided.")
            
        # Remove gs:// prefix if present
        staging_bucket = staging_bucket.replace('gs://', '')
        if data_bucket:
            data_bucket = data_bucket.replace('gs://', '')
        
        aiplatform.init(
            project=project_id, 
            location=location, 
            staging_bucket=f"gs://{staging_bucket}"
        )
        self.project_id = project_id
        self.location = location
        self.staging_bucket = staging_bucket
        self.data_bucket = data_bucket

    def _extract_function_names(self, function_code: str) -> List[str]:
        """
        Extract function names from a string containing Python function definitions.
        
        Args:
            function_code (str): String containing Python function definitions
            
        Returns:
            List[str]: List of function names found in the code
            
        Raises:
            ValueError: If no functions are found or if the code is invalid
        """
        try:
            # Parse the code into an AST
            tree = ast.parse(function_code)
            
            # Find all function definitions
            function_names = []
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    function_names.append(node.name)
            
            if not function_names:
                # Fallback to regex if AST doesn't work
                regex_matches = re.findall(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', function_code)
                if regex_matches:
                    function_names = regex_matches
                else:
                    raise ValueError("No function definitions found in the provided code")
            
            return function_names
            
        except SyntaxError as e:
            raise ValueError(f"Invalid Python syntax in function code: {e}")
        except Exception as e:
            # Fallback to regex approach
            regex_matches = re.findall(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', function_code)
            if regex_matches:
                return regex_matches
            else:
                raise ValueError(f"Could not extract function names: {e}")

    def _get_main_function_name(self, function_code: str) -> str:
        """
        Get the main processing function name from the function code.
        If multiple functions are defined, returns the first one.
        
        Args:
            function_code (str): String containing Python function definitions
            
        Returns:
            str: The name of the main processing function
        """
        function_names = self._extract_function_names(function_code)
        
        if len(function_names) == 1:
            return function_names[0]
        elif len(function_names) > 1:
            # If multiple functions, look for common patterns or return the first one
            # You could add logic here to identify the "main" function if needed
            return function_names[0]
        else:
            raise ValueError("No processing function found in the provided code")

    def _monitor_job_progress(self, input_bucket: str, output_bucket: str):
        """Monitor job progress by counting files in output bucket"""
        client = storage.Client()
        input_files = list(client.list_blobs(input_bucket))
        total_files = len(input_files)
        
        with tqdm(total=total_files, desc="Processing files") as pbar:
            processed_count = 0
            while processed_count < total_files:
                # Count processed files in output bucket
                new_count = len(list(client.list_blobs(output_bucket)))
                if new_count > processed_count:
                    pbar.update(new_count - processed_count)
                    processed_count = new_count
                time.sleep(5)  # Check every 5 seconds
    
    def submit_job(
        self,
        processing_fn: str,
        input_folder: str,
        output_folder: str,
        requirements: List[str] = None,
        input_bucket: str = None,
        output_bucket: str = None,
        workers: int = 1,
        machine_config: Optional[MachineConfig] = None,
        job_config: Optional[JobConfig] = None,
        batch_size: int = 1,
        show_progress: bool = True
    ):
        """
        Submit a processing job to Vertex AI
        
        Args:
            processing_fn (str): The function to be executed
            input_folder (str): The folder path for input files (e.g. "raw-data/")
            output_folder (str): The folder path for output files (e.g. "landmarks/")
            input_bucket (str, optional): Override the default data bucket for input
            output_bucket (str, optional): Override the default data bucket for output
            workers (int): The number of workers to use
            machine_config (Optional[MachineConfig]): The machine configuration
            job_config (Optional[JobConfig]): The job configuration
            batch_size (int): The batch size to use
            show_progress (bool): Whether to show a progress bar in notebooks
        """
        # Use default data bucket if not overridden
        input_bucket = input_bucket or self.data_bucket
        output_bucket = output_bucket or self.data_bucket

        if not input_bucket or not output_bucket:
            raise ValueError("No data bucket specified. Either provide it during initialization or in submit_job()")

        machine_config = machine_config or MachineConfig()
        job_config = job_config or JobConfig()

        # Extract the main function name from the processing function
        try:
            main_function_name = self._get_main_function_name(processing_fn)
        except Exception as e:
            raise ValueError(f"Failed to extract function name from processing_fn: {e}")

        # Add pip install commands to script
        requirements_install = ""
        if requirements:
            requirements_install = "pip install " + " ".join(requirements)

        # Define the script to be executed
        script_contents = f'''
import os
from google.cloud import storage
import tempfile
import shutil
import math
import subprocess
import time

# Install requirements
# subprocess.run("{requirements_install}", shell=True, check=True)
# Install ffmpeg
subprocess.run(["apt-get", "update"])
subprocess.run(["apt-get", "install", "-y", "ffmpeg"])

# Verify installation
subprocess.run(["ffmpeg", "-version"])

{processing_fn}
    
def process_batch(start_idx, end_idx, input_bucket, output_bucket, input_folder, output_folder):
    client = storage.Client()
    bucket = client.bucket(input_bucket)
    blobs = list(bucket.list_blobs(prefix=input_folder))[start_idx:end_idx]
    
    for blob in blobs:
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = os.path.join(temp_dir, blob.name.split("/")[-1])
            blob.download_to_filename(input_path)
            
            try:
                output_path = {main_function_name}(input_path, temp_dir)
                output_blob = client.bucket(output_bucket).blob(
                    output_folder + "processed_" + os.path.basename(blob.name)
                )
                output_blob.upload_from_filename(output_path)
            
            finally:
                if os.path.exists(input_path):
                    os.remove(input_path)
                shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    if {workers} > 1:
        parser.add_argument("--worker-id", type=int, default=0)
        parser.add_argument("--num-workers", type=int, required=True)
        args = parser.parse_args()
        
        # Get worker ID from environment variable if not provided via args
        if args.worker_id == 0 and 'CLOUD_ML_TASK_ID' in os.environ:
            task_id = int(os.environ['CLOUD_ML_TASK_ID'])
            worker_pool_id = int(os.environ.get('CLOUD_ML_WORKER_POOL_ID', 0))
            # Master pool (ID 0) gets worker_id 0, worker pool (ID 1) gets task_id + 1
            args.worker_id = task_id + 1 if worker_pool_id == 1 else 0
        
        total_items = len(list(storage.Client().list_blobs("{input_bucket}")))
        items_per_worker = math.ceil(total_items / args.num_workers)
        start_idx = args.worker_id * items_per_worker
        end_idx = min(start_idx + items_per_worker, total_items)
    else:
        args = parser.parse_args()
        start_idx = 0
        end_idx = len(list(storage.Client().list_blobs("{input_bucket}")))
    
    for batch_start in range(start_idx, end_idx, {batch_size}):
        batch_end = min(batch_start + {batch_size}, end_idx)
        process_batch(
            batch_start,
            batch_end,
            "{input_bucket}",
            "{output_bucket}",
            "{input_folder}",
            "{output_folder}"
        )
'''

        # Define worker pool specifications
        worker_pool_specs = [
            # Master worker pool (always 1 replica)
            {
                "machine_spec": {
                    "machine_type": machine_config.machine_type,
                    "accelerator_type": machine_config.accelerator_type if machine_config.accelerator_type else None,
                    "accelerator_count": machine_config.accelerator_count if machine_config.accelerator_type else 0
                },
                "replica_count": 1,  # Master pool always has 1 replica
                "container_spec": {
                    "image_uri": "europe-docker.pkg.dev/vertex-ai/training/tf-cpu.2-14.py310:latest",
                    "command": ["python", "-c", script_contents],
                    "args": [f"--num-workers={workers}"] if workers > 1 else []
                },
                "disk_spec": {
                    "boot_disk_type": "pd-ssd",
                    "boot_disk_size_gb": machine_config.disk_size_gb
                }
            }
        ]

        # Add worker pool for additional workers if needed
        if workers > 1:
            worker_pool_specs.append({
                "machine_spec": {
                    "machine_type": machine_config.machine_type,
                    "accelerator_type": machine_config.accelerator_type if machine_config.accelerator_type else None,
                    "accelerator_count": machine_config.accelerator_count if machine_config.accelerator_type else 0
                },
                "replica_count": workers - 1,  # Remaining workers
                "container_spec": {
                    "image_uri": "europe-docker.pkg.dev/vertex-ai/training/tf-cpu.2-14.py310:latest",
                    "command": ["python", "-c", script_contents],
                    "args": [f"--num-workers={workers}"]
                },
                "disk_spec": {
                    "boot_disk_type": "pd-ssd",
                    "boot_disk_size_gb": machine_config.disk_size_gb
                }
            })

        # Create custom job
        job = aiplatform.CustomJob(
            display_name=f"video-process",
            worker_pool_specs=worker_pool_specs,
            staging_bucket=self.staging_bucket
        )

        # Set job options based on JobConfig
        job_kwargs = {
            "sync": True,  # Wait for the job to complete
        }

        if job_config.timeout_days:
            job_kwargs["timeout"] = int(job_config.timeout_days * 24 * 60 * 60)  # Convert days to seconds

        if show_progress:
            # Start job and progress monitoring in separate threads
            job_thread = Thread(target=job.run, kwargs=job_kwargs, daemon=True)
            progress_thread = Thread(
                target=self._monitor_job_progress,
                args=(input_bucket, output_bucket),
                daemon=True
            )
            
            job_thread.start()
            progress_thread.start()
            job_thread.join()
            progress_thread.join()
        else:
            # Run job without progress monitoring
            job.run(**job_kwargs)
            
        return job