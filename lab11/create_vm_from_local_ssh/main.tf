provider "google" {
  project     = var.project_id
  region      = "us-central1"
  zone        = "us-central1-c"
}
resource "google_compute_network" "vpc_network" {
  name                    = "my-custom-mode-network"
  auto_create_subnetworks = false
  mtu                     = 1460
}

resource "google_compute_subnetwork" "default" {
  name          = "my-custom-subnet"
  ip_cidr_range = "10.0.1.0/24"
  region        = "us-central1"
  network       = google_compute_network.vpc_network.id
}
# Create a single Compute Engine instance
resource "google_compute_instance" "default" {
  name         = "ada-vm"
  machine_type = "f1-micro"
  zone         = "us-central1-c"
  tags         = ["ssh"]

  boot_disk {
    initialize_params {
      image = "ubuntu-2204-jammy-v20240501"
    }
  }

  metadata = {
    ssh-keys = "${var.gce_ssh_user}:${file(var.gce_ssh_pub_key_file)}"
  }
 # Install Flask
  metadata_startup_script = "sudo apt-get update; sudo apt-get install -yq build-essential python3-pip rsync; pip install flask"

  network_interface {
    subnetwork = google_compute_subnetwork.default.id

    access_config {
      # Include this section to give the VM an external IP address
    }
  }
}

resource "google_compute_firewall" "ssh" {
  name = "allow-ssh"
  allow {
    ports    = ["22"]
    protocol = "tcp"
  }
  direction     = "INGRESS"
  network       = google_compute_network.vpc_network.id
  priority      = 1000
  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["ssh"]
}

resource "google_compute_firewall" "flask" {
  name    = "flask-app-firewall"
  network = google_compute_network.vpc_network.id

  allow {
    protocol = "tcp"
    ports    = ["5000"]
  }
  source_ranges = ["0.0.0.0/0"]
}


resource "null_resource" "remote_script" {
  connection {
    type        = "ssh"
    host        = google_compute_instance.default.network_interface.0.access_config.0.nat_ip
    user        = var.gce_ssh_user
    agent       = true
  }

  provisioner "remote-exec" {
    inline = [
      "echo '${file("testscript.sh")}' > /home/${var.gce_ssh_user}/testscript.sh",
      "chmod +x /home/${var.gce_ssh_user}/testscript.sh",  # Make the script executable
      "/home/${var.gce_ssh_user}/testscript.sh"
    ]
  }
  depends_on = [
    google_compute_firewall.ssh
  ]
}