# resource "google_container_registry" "registry" {
#   project  = local.project_id
#   location = local.region
# }

# resource "google_storage_bucket_iam_member" "viewer" {
#   bucket = google_container_registry.registry.id
#   role = "roles/storage.objectViewer"
#   member = "user:jane@example.com"
# }