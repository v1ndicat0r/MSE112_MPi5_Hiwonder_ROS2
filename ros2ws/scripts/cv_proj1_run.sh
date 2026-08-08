#!/bin/bash

cd ..

source ./overlay_source.sh

x-terminal-emulator -e bash -c "ros2 run vision_stack image_publisher;exec bash" & x-terminal-emulator -e bash -c "ros2 run vision_stack line_tracking;exec bash"
