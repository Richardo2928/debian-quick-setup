# My Quick Debian Setup
## Description

My Quick Debian Setup is a setup script for Debian that automates the installation of common tools and environments, designed for both general users and developers. This script allows users to quickly select and configure applications, development environments, and servers through a simple menu.
## Main Features

- Installation of common applications: Opera, OneDrive, Obsidian, Homebrew, SAMBA, curl, and more.
- Setup of development environments: C/C++, Python, Node.js, and more.
- Basic configuration of servers: SSH, Samba, Apache, MySQL, and others.
- Modular and flexible process that allows users to select only the tools they need.
- Interactive whiptail-based user interface for an easy experience.

## Prerequisites

- Debian 12 (or derivatives) or any Linux distribution based on apt.
- Internet connection to download the required tools.

## How to Use

1. Clone the repository:
```
git clone https://github.com/Richardo2928/debian-quick-setup-richardo2928.git
cd my-quick-debian-setup
```

```
# or download the repo as a ZIP file and extract it:

wget https://github.com/Richardo2928/debian-quick-setup/archive/refs/heads/main.zip && unzip main.zip && cd debian-quick-setup-main
```
2. Make the script executable:
```
chmod +x setup.sh
```
3. Run the script:
```
./setup.sh
```