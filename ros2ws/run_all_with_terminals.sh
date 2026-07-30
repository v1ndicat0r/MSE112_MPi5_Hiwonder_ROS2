#!/bin/bash

source overlay_source.sh

x-terminal-emulator -e bash -c "ros2 run opencv2_nodes image_publisher" & x-terminal-emulator -e bash -c "ros2 run opencv2_nodes bin_mask" & x-terminal-emulator -e bash -c "ros2 run opencv2_nodes line_recog" & x-terminal-emulator -e bash -c "ros2 run controls_core main_control_node" & x-terminal-emulator -e bash -c "ros2 run hiwonder_board hiwonder_board_node"
