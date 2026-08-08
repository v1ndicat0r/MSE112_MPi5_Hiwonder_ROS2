#!/bin/bash

cd ..

source ./overlay_source.sh

x-terminal-emulator -e bash -c "ros2 run hiwonder_board hiwonder_board_node;exec bash"



