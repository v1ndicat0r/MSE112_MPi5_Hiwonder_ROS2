#!/bin/bash

source overlay_source.sh

ros2 run opencv2_nodes image_publisher & ros2 run opencv2_nodes bin_mask & ros2 run opencv2_nodes line_recog & ros2 run controls_core main_control_node & ros2 run hiwonder_board hiwonder_board_node
