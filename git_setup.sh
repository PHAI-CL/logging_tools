#!/bin/bash
apt-get update
apt -y install git
git config --global user.name "PHAI-CL"
git config --global user.email "CL11269@protonmail.com"
apt update
apt -y install gh
gh auth login
git config --global --add safe.directory /opt/project
# Install dependencies for package first
pip install git+https://github.com/PHAI-CL/path_finder.git
pip install git+https://github.com/PHAI-CL/connection_tools.git
# Create editable install (to load package from within itself for testing)
pip install -e .     
