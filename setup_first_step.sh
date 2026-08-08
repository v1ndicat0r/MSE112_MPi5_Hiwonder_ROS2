#!/bin/bash
sudo -v


sudo sh -c '
grep -qxF "[pi5]" /boot/firmware/config.txt || echo "[pi5]" >> /boot/firmware/config.txt
grep -qxF "dtparam=uart0=on" /boot/firmware/config.txt || echo "dtparam=uart0=on" >> /boot/firmware/config.txt
grep -qxF "enable_uart=1" /boot/firmware/config.txt || echo "enable_uart=1" >> /boot/firmware/config.txt
'

sudo dpkg -i /home/admin/MSE112_MPi5_Hiwonder_ROS2/foxglove_installation/foxglove-studio-latest-linux-arm64.deb

sudo apt install ros-lyrical-foxglove-bridge

printf "Step 1 complete! Reboot now and then run Step 2." > /dev/tty



