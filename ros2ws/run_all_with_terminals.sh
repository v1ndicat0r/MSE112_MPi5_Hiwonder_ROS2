#!/bin/bash

source overlay_source.sh

x-terminal-emulator -e bash -c "ros2 run vision_stack image_publisher;exec bash" & x-terminal-emulator -e bash -c "ros2 run vision_stack bin_mask; exec bash" & x-terminal-emulator -e bash -c "ros2 run vision_stack line_recog; exec bash" & x-terminal-emulator -e bash -c "ros2 run core main; exec bash" & x-terminal-emulator -e bash -c "ros2 run hiwonder_board hiwonder_board_node; exec bash"
