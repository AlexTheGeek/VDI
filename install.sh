#!/bin/sh

# Check if the script is run as root
if [ "$(id -u)" -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

# Installing dependencies
echo "Installing dependencies"
apt update
apt install python3=3.11.2 git -y

# Asking for pip or pipx
echo "Do you want to install pip or pipx?"
echo "1. pip"
echo "2. pipx"
read -p "Enter your choice: " choice

if [ $choice -eq 1 ]; then
    echo "Installing pip"
    apt install python3-pip -y
    echo "Installing python packages"
    pip3 install Flask==3.0.0 gunicorn==20.1.0 --break-system-packages
elif [ $choice -eq 2 ]; then
    echo "Installing pipx"
    python3 -m pip install pipx
    python3 -m pipx ensurepath
    echo "Installing python packages"
    pipx install Flask==3.0.0 gunicorn==20.1.0
else
    echo "Invalid choice"
    exit 1
fi

# Create a the vdi user for the application
echo "Creating the vdi user"
useradd -m -s /bin/bash vdi

# Creating the vdi directory
echo "Creating the vdi directory"
mkdir -p /home/vdi/VDI-APP
mkdir -p /var/log/VDI/APP
touch /var/log/VDI/API/access.log /var/log/VDI/API/error.log

# Cloning the repository
echo "Cloning the repository"
git clone https://github.com/AlexTheGeek/VDI.git /home/vdi/VDI-APP

# Changing the ownership of the vdi directory
echo "Changing the ownership of the vdi directory"
chown -R vdi:vdi /home/vdi/VDI-APP
chown -R vdi:vdi /var/log/VDI/APP

echo "Creating the service file"
cp /home/vdi/VDI-APP/app-vdi.service /etc/systemd/system/app-vdi.service

# Starting the service
echo "Starting the service"
systemctl daemon-reload
systemctl start app-vdi
systemctl enable app-vdi











