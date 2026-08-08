#!/bin/bash
sudo -v



sudo sh -c 'printf "%s\n" "KERNEL==\"ttyAMA0\", MODE=\"0666\"" > /etc/udev/rules.d/99-tty-permissions.rules'

sudo sh -c 'printf "%s\n" "KERNEL==\"video0\", MODE=\"0666\"" > /etc/udev/rules.d/99-video-permissions.rules'

sudo udevadm control --reload-rules

sudo udevadm trigger



sudo apt update

sudo apt install -y python3-smbus
sudo apt install python3-smbus2





printf "Step 2 complete!" > /dev/tty
