# output "vertex_ai_endpoint_id" {
#   description = "The ID of the Vertex AI endpoint"
#   value       = module.vertex_ai.endpoint_id
# }

output "data_bucket" {
  description = "The name of the main data bucket"
  value       = module.storage.data_bucket
}
