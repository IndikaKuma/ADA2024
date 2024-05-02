# Output variable definitions

output "Public-IP" {
  description = "Public-IP of the VM"
  value = google_compute_instance.default.network_interface.0.access_config.0.nat_ip
}