#!/bin/bash

source overlay_source.sh

ros2 run vision_stack image_publisher & ros2 run vision_stack bin_mask & ros2 run vision_stack line_recog & ros2 run core main & ros2 run hiwonder_board hiwonder_board_node
