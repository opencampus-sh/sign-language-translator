# app/vertex_ai_client.py
from google.cloud import aiplatform
from google.cloud import aiplatform_v1
import json
from google.api import httpbody_pb2
from typing import Dict, Any

class VertexAIClient:
    def __init__(self, project_id: str, location: str, endpoint_id: str):
        self.project_id = project_id
        self.location = location
        self.endpoint_id = endpoint_id
        self.client = aiplatform_v1.PredictionServiceClient(
            client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"}
        )
        self.endpoint = f"projects/{project_id}/locations/{location}/endpoints/{endpoint_id}"

    def predict(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send prediction request to Vertex AI endpoint
        
        Args:
            input_data: Dictionary containing the input data for prediction
            
        Returns:
            Dictionary containing the prediction results
        """
        json_data = json.dumps(input_data)
        
        http_body = httpbody_pb2.HttpBody(
            data=json_data.encode("utf-8"),
            content_type="application/json",
        )
        
        request = aiplatform_v1.RawPredictRequest(
            endpoint=self.endpoint,
            http_body=http_body,
        )
        
        response = self.client.raw_predict(request)
        return json.loads(response.data)

# Usage example
if __name__ == "__main__":
    client = VertexAIClient(
        project_id="your-project",
        location="europe-west3",
        endpoint_id="your-endpoint-id"
    )
    
    # Example prediction request
    result = client.predict({
        "sequences": "Your input text",
        "candidate_labels": ["label1", "label2"]
    })
    print(result)
    