def upload_csv_and_prepare_batch_data(csv_file_path: str, project_id: str, environment: str = "dev"):
    """
    Upload CSV file to Google Cloud Storage and create individual row files for batch processing.
    
    Args:
        csv_file_path: Local path to the CSV file
        project_id: GCP project ID
        environment: Environment name (dev, prod)
    
    Returns:
        str: Number of rows processed
    """
    import pandas as pd
    import json
    import os
    from google.cloud import storage
    
    # Initialize storage client
    client = storage.Client(project=project_id)
    bucket_name = f"{project_id}-{environment}-data"
    bucket = client.bucket(bucket_name)
    
    # Read CSV file
    print(f"Reading CSV file: {csv_file_path}")
    df = pd.read_csv(csv_file_path)
    
    # Filter rows that have valid webm URLs
    df_valid = df.dropna(subset=['webm'])
    print(f"Found {len(df_valid)} rows with valid video URLs")
    
    # Upload original CSV file
    csv_blob = bucket.blob("raw-data/tagesschau_sign_language_video_links.csv")
    csv_blob.upload_from_filename(csv_file_path)
    print(f"Uploaded CSV to gs://{bucket_name}/raw-data/tagesschau_sign_language_video_links.csv")
    
    # Create individual JSON files for each row (for batch processing)
    print("Creating individual row files for batch processing...")
    for idx, row in df_valid.iterrows():
        # Convert row to JSON string, handling NaN values properly
        row_data = row.to_dict()
        # Replace NaN values with None (which becomes null in JSON)
        row_data = {k: (None if pd.isna(v) else v) for k, v in row_data.items()}
        row_json = json.dumps(row_data, ensure_ascii=False)
        
        # Create a file for each row
        row_filename = f"csv-rows/row_{idx:06d}.json"
        row_blob = bucket.blob(row_filename)
        row_blob.upload_from_string(row_json, content_type='application/json')
        
        if idx % 100 == 0:
            print(f"Uploaded row {idx}")
    
    print(f"Successfully uploaded {len(df_valid)} row files to gs://{bucket_name}/csv-rows/")
    return len(df_valid)


def list_csv_rows(project_id: str, environment: str = "dev", limit: int = None):
    """
    List the CSV row files available for processing.
    
    Args:
        project_id: GCP project ID
        environment: Environment name
        limit: Maximum number of files to list
    
    Returns:
        list: List of blob names
    """
    from google.cloud import storage
    
    client = storage.Client(project=project_id)
    bucket_name = f"{project_id}-{environment}-data"
    bucket = client.bucket(bucket_name)
    
    blobs = list(bucket.list_blobs(prefix="csv-rows/"))
    if limit:
        blobs = blobs[:limit]
    
    print(f"Found {len(blobs)} CSV row files in gs://{bucket_name}/csv-rows/")
    return [blob.name for blob in blobs] 