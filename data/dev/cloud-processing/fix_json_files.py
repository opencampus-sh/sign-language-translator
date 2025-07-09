def fix_existing_json_files(project_id: str, environment: str = "dev"):
    """
    Fix existing JSON files in Google Cloud Storage by replacing NaN values with null.
    
    Args:
        project_id: GCP project ID
        environment: Environment name (dev, prod)
    """
    import json
    import pandas as pd
    from google.cloud import storage
    
    # Initialize storage client
    client = storage.Client(project=project_id)
    bucket_name = f"{project_id}-{environment}-data"
    bucket = client.bucket(bucket_name)
    
    # List all JSON files in csv-rows/
    blobs = list(bucket.list_blobs(prefix="csv-rows/"))
    json_blobs = [blob for blob in blobs if blob.name.endswith('.json')]
    
    print(f"Found {len(json_blobs)} JSON files to fix")
    
    fixed_count = 0
    for blob in json_blobs:
        try:
            # Download the blob content
            content = blob.download_as_text()
            
            # Try to parse as JSON - if it fails, it probably has NaN values
            try:
                data = json.loads(content)
                # If it parses successfully, skip it
                continue
            except json.JSONDecodeError:
                # If it fails, it likely has NaN values - fix them
                pass
            
            # Fix NaN values by replacing them with null
            # This is a bit hacky but works for this specific case
            fixed_content = content.replace(': NaN', ': null')
            
            # Try to parse the fixed content
            try:
                data = json.loads(fixed_content)
                # If successful, upload the fixed version
                blob.upload_from_string(fixed_content, content_type='application/json')
                fixed_count += 1
                
                if fixed_count % 100 == 0:
                    print(f"Fixed {fixed_count} files")
                    
            except json.JSONDecodeError as e:
                print(f"Could not fix {blob.name}: {e}")
                
        except Exception as e:
            print(f"Error processing {blob.name}: {e}")
    
    print(f"✅ Fixed {fixed_count} JSON files")
    return fixed_count


def verify_json_files(project_id: str, environment: str = "dev", sample_size: int = 10):
    """
    Verify that JSON files are valid by sampling a few files.
    
    Args:
        project_id: GCP project ID
        environment: Environment name
        sample_size: Number of files to check
    """
    import json
    from google.cloud import storage
    
    client = storage.Client(project=project_id)
    bucket_name = f"{project_id}-{environment}-data"
    bucket = client.bucket(bucket_name)
    
    # List JSON files
    blobs = list(bucket.list_blobs(prefix="csv-rows/"))
    json_blobs = [blob for blob in blobs if blob.name.endswith('.json')]
    
    if not json_blobs:
        print("No JSON files found")
        return
    
    # Sample some files
    import random
    sample_blobs = random.sample(json_blobs, min(sample_size, len(json_blobs)))
    
    valid_count = 0
    for blob in sample_blobs:
        try:
            content = blob.download_as_text()
            data = json.loads(content)
            valid_count += 1
            print(f"✅ {blob.name} - Valid JSON")
            
            # Show sample data
            if valid_count == 1:
                print(f"   Sample content: {json.dumps(data, indent=2)[:200]}...")
                
        except json.JSONDecodeError as e:
            print(f"❌ {blob.name} - Invalid JSON: {e}")
        except Exception as e:
            print(f"❌ {blob.name} - Error: {e}")
    
    print(f"\nResult: {valid_count}/{len(sample_blobs)} files are valid JSON")
    return valid_count == len(sample_blobs) 