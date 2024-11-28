from google.cloud import aiplatform
from google.cloud import storage
import math
from dataclasses import dataclass
from typing import Optional

@dataclass
class MachineConfig:
    machine_type: str = "n1-standard-4"
    accelerator_type: Optional[str] = None
    accelerator_count: int = 0
    disk_size_gb: int = 100

@dataclass
class JobConfig:
    provisioning_model: Literal["DEDICATED", "SPOT"] = "DEDICATED"
    restart_on_failure: bool = True
    timeout_days: Optional[float] = None

class CloudProcessor:
    def __init__(self, project_id: str, location: str = "us-central1"):
        aiplatform.init(project=project_id, location=location)
        self.project_id = project_id
        self.location = location
    
    def submit_job(
        self,
        processing_fn: str,
        input_bucket: str,
        output_bucket: str,
        workers: int = 1,
        machine_config: Optional[MachineConfig] = None,
        job_config: Optional[JobConfig] = None,
        batch_size: int = 1
    ):
        machine_config = machine_config or MachineConfig()
        job_config = job_config or JobConfig()

        # Rest of the script_contents remains the same as previous version
        script_contents = f'''
import os
from google.cloud import storage
import tempfile
import shutil

{processing_fn}

def process_batch(start_idx, end_idx, input_bucket, output_bucket):
    client = storage.Client()
    blobs = list(client.list_blobs(input_bucket))[start_idx:end_idx]
    
    for blob in blobs:
        # Create temporary directory for this video
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = os.path.join(temp_dir, blob.name.split("/")[-1])
            
            # Download video
            blob.download_to_filename(input_path)
            
            try:
                # Process video
                output_path = process_single_video(input_path, temp_dir)
                
                # Upload result
                output_blob = client.bucket(output_bucket).blob(
                    f"processed_{blob.name}"
                )
                output_blob.upload_from_filename(output_path)
            
            finally:
                # Cleanup
                if os.path.exists(input_path):
                    os.remove(input_path)
                shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    if {workers} > 1:
        parser.add_argument("--worker-id", type=int, required=True)
        parser.add_argument("--num-workers", type=int, required=True)
        args = parser.parse_args()
        
        total_items = len(list(storage.Client().list_blobs("{input_bucket}")))
        items_per_worker = math.ceil(total_items / args.num_workers)
        start_idx = args.worker_id * items_per_worker
        end_idx = min(start_idx + items_per_worker, total_items)
    else:
        args = parser.parse_args()
        start_idx = 0
        end_idx = len(list(storage.Client().list_blobs("{input_bucket}")))
    
    # Process in batches
    for batch_start in range(start_idx, end_idx, {batch_size}):
        batch_end = min(batch_start + {batch_size}, end_idx)
        process_batch(
            batch_start,
            batch_end,
            "{input_bucket}",
            "{output_bucket}"
        )
'''

        machine_spec = {
            "machine_type": machine_config.machine_type,
            "disk_size_gb": machine_config.disk_size_gb,
        }
        
        if machine_config.accelerator_type:
            machine_spec.update({
                "accelerator_type": machine_config.accelerator_type,
                "accelerator_count": machine_config.accelerator_count
            })
        
        container_spec = {
            "image_uri": "us-docker.pkg.dev/vertex-ai/training/pytorch-cpu.1-13:latest",
            "command": ["python", "-c", script_contents],
        }
        
        if workers > 1:
            container_spec["args"] = [
                f"--worker-id=$(JOB_ID)",
                f"--num-workers={workers}",
            ]
        
        worker_pool_specs = [{
            "machine_spec": machine_spec,
            "replica_count": workers,
            "container_spec": container_spec,
        }]

        scheduling = aiplatform.JobScheduling(
            provisioning_model=job_config.provisioning_model,
            restart_job_on_worker_restart=job_config.restart_on_failure
        )
        
        if job_config.timeout_days:
            scheduling.timeout = f"{job_config.timeout_days * 24}h"

        job = aiplatform.CustomJob(
            display_name=f"video-process",
            worker_pool_specs=worker_pool_specs,
            scheduling=scheduling
        )
        
        job.run()
        return job