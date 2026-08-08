#!/bin/bash

cd ..

source build_source.sh

colcon build --packages-select vision_stack

x-terminal-emulator -e bash -c "ros2 run vision_stack image_publisher;exec bash" & x-terminal-emulator -e bash -c "ros2 run vision_stack line_tracking;exec bash"
