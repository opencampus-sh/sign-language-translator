output "vertex_ai_endpoint_id" {
  description = "The ID of the Vertex AI endpoint"
  value       = module.vertex_ai.endpoint_id
}

output "training_data_bucket" {
  description = "The name of the training data bucket"
  value       = module.storage.training_data_bucket
}
