#!/bin/bash
apt-get update
apt -y install git
git config --global user.name "PHAI-CL"
git config --global user.email "CL11269@protonmail.com"
apt update
apt -y install gh
gh auth login