#!/bin/bash

cd ..

source build_source.sh

colcon build --packages-select core

x-terminal-emulator -e bash -c "ros2 run core main;exec bash"
