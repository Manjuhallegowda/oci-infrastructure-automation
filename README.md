# OCI Infrastructure Automation (Cloud Resource Hunter)

## Overview
A Python-based automation tool designed to programmatically "hunt" and provision Oracle Cloud (OCI) ARM instances, bypassing high-demand resource limitations in the Always Free tier.

## Key Features
- **Automated Provisioning:** Uses OCI SDK to monitor and claim resources.
- **Persistence:** Configured with systemd for 100% uptime on headless Linux.
- **Security:** Integrated SAST (Bandit) and automated CI/CD via GitHub Actions.

## Setup
1. Clone the repo: `git clone https://github.com/Manjuhallegowda/oci-infrastructure-automation.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Configure OCI CLI with your credentials.
4. Run the hunter: `python src/oci_hunter.py`

## CI/CD Pipeline
Every push triggers a GitHub Action that performs:
1. **Linting** (flake8)
2. **Security Scanning** (Bandit)
3. **Unit Testing** (PyTest)