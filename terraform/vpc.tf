# Create a VPC
resource "google_compute_network" "bigquery_vpc" {
  name                    = "${local.name_prefix}-network"
  auto_create_subnetworks = "false"

}

# Create a Subnet
resource "google_compute_subnetwork" "bigquery-subnet" {
  name          = "${local.name_prefix}-subnet-1"
  ip_cidr_range = "10.20.0.0/24"
  network       = google_compute_network.bigquery_vpc.name
  region        = local.region
}

## Create Cloud Router

resource "google_compute_router" "router" {
  project = local.project_id
  name    = "${local.name_prefix}-nat-router"
  network = google_compute_network.bigquery_vpc.name
  region  = local.region
  depends_on = [ google_compute_network.bigquery_vpc ]
}

## Create Nat Gateway

resource "google_compute_router_nat" "nat" {
  name                               = "${local.name_prefix}-nat"
  router                             = google_compute_router.router.name
  region                             = local.region
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"

  log_config {
    enable = true
    filter = "ERRORS_ONLY"
  }
}
