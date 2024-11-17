import os

class DevelopmentConfig:
    # Vertex AI settings
    VERTEX_AI = {
        'project_id': os.getenv('GCP_PROJECT_ID'),
        'location': os.getenv('GCP_LOCATION', 'europe-west3'),
        'endpoint_id': os.getenv('VERTEX_AI_ENDPOINT_ID'),
        'batch_size': 1,
        'timeout_seconds': 30
    }

    # Mock model settings for offline development
    MOCK_MODEL = {
        'enabled': os.getenv('USE_MOCK_MODEL', 'true').lower() == 'true',
        'latency_ms': 500  # Simulated latency
    }

    # Feature flags for development
    FEATURES = {
        'use_video_cache': True,  # Cache processed videos
        'debug_logging': True,    # Enhanced logging
        'mock_responses': True    # Use mock responses when needed
    } 