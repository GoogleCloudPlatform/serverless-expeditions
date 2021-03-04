output "service_url" {
  value = google_cloud_run_service.cats.status[0].url
}