#!/bin/bash

cd ..

source build_source.sh

colcon build --packages-select hiwonder_board

x-terminal-emulator -e bash -c "ros2 run hiwonder_board hiwonder_board_node;exec bash"
