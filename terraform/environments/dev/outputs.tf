output "cloudrun_service_url" {
  description = "The URL of the deployed Cloud Run service"
  value       = module.cloudrun.service_url
}

output "cloudrun_service_name" {
  description = "The name of the Cloud Run service"
  value       = module.cloudrun.service_name
}
