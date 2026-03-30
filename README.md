# OCI Infrastructure Automation (Cloud Resource Hunter)

## Overview
[cite_start]A Python-based automation tool designed to programmatically "hunt" and provision Oracle Cloud (OCI) ARM instances, bypassing high-demand resource limitations in the Always Free tier[cite: 27, 29].

## Key Features
- [cite_start]**Automated Provisioning:** Uses OCI SDK to monitor and claim resources[cite: 29].
- [cite_start]**Persistence:** Configured with systemd for 100% uptime on headless Linux[cite: 31].
- [cite_start]**Security:** Integrated SAST (Bandit) and automated CI/CD via GitHub Actions[cite: 15, 34].

## Setup
1. Clone the repo: `git clone https://github.com/Manjuhallegowda/oci-infrastructure-automation.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Configure OCI CLI with your credentials.
4. Run the hunter: `python src/oci_hunter.py`

## CI/CD Pipeline
Every push triggers a GitHub Action that performs:
1. **Linting** (flake8)
2. [cite_start]**Security Scanning** (Bandit) [cite: 15, 34]
3. [cite_start]**Unit Testing** (PyTest) [cite: 15, 35]