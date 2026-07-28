#!/bin/bash

source overlay_source.sh

colcon build --packages-select hiwonder_board

ros2 run hiwonder_board hiwonder_board_node
