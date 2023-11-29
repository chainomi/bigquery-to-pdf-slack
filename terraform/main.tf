provider "google" {
  project     = local.project_id
  region      = local.region
  credentials = "../useful-circle-358120-5ebbc15b4e95.json"
}

locals {
    name_prefix = "big-query-sql"
    region = "us-central1"
    project_id = "useful-circle-358120"

    # roles below for nodes to pull images from container registry / artifact registry
    node_sa_roles = [
        "roles/artifactregistry.reader",
        "roles/storage.objectAdmin"
    ]
    min_node_count = 2
    max_node_count = 4
}


# Default service account for nodes

resource "google_service_account" "default_node" {
  account_id   = "${local.name_prefix}-gke-node-sa"
  display_name = "Service Account"
}


resource "google_project_iam_member" "default_sa_bindings" {
    for_each = toset(local.node_sa_roles)

    project = local.project_id
    role    = each.value
    member  = "serviceAccount:${google_service_account.default_node.email}"
  
}

resource "google_container_cluster" "primary" {
  name = "${local.name_prefix}-cluster"
  location = local.region
  remove_default_node_pool = true
  initial_node_count = 1

  network    = google_compute_network.bigquery_vpc.name
  subnetwork = google_compute_subnetwork.bigquery-subnet.name


  workload_identity_config {
    workload_pool = "${local.project_id}.svc.id.goog"
  }
}


resource "google_container_node_pool" "primary_preemptible_nodes" {
  name       = "${local.name_prefix}-node-pool"
  location   = local.region
  cluster    = google_container_cluster.primary.name
  node_count = 1

  node_config {

    preemptible  = true
    machine_type = "e2-medium"

    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    service_account = google_service_account.default_node.email
    oauth_scopes    = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }

  # Autoscaling
  autoscaling {
    min_node_count = local.min_node_count
    max_node_count = local.max_node_count
  }

}



# Worker identity setup from here 

## Create service account
resource "google_service_account" "cluster_service_account" {
  account_id = "${local.name_prefix}-sa"
  display_name = "Service account for testing bigquery cron job"

}


# Service account roles - roles to run app

locals {
    wi_roles = [
        "roles/bigquery.jobUser",
        "roles/bigquery.dataViewer",
        "roles/storage.insightsCollectorService",
        "roles/storage.objectUser",
        "roles/storage.objectCreator"
    ]
}


resource "google_project_iam_member" "wi_sa_bindings" {
    for_each = toset(local.wi_roles)

    project = local.project_id
    role    = each.value
    member  = "serviceAccount:${google_service_account.cluster_service_account.email}"
  
}

# resource "google_service_account_iam_member" "main" {
#     service_account_id = google_service_account.cluster_service_account.name
#     role = "roles/iam.workloadIdentityUser"
#     member = "serviceAccount:${local.project_id}.svc.id.goog"
  
# }

resource "google_service_account_iam_binding" "workload_identity_binding" {
  service_account_id = google_service_account.cluster_service_account.name
  role = "roles/iam.workloadIdentityUser"
  members = [
    "serviceAccount:${local.project_id}.svc.id.goog[bigquery/bigquery-sa]"
    # "serviceAccount:${var.project}.svc.id.goog[<namespace>/<ksa>]"
  ]
}
