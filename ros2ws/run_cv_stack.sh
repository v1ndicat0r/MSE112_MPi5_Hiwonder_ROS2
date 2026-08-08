#!/bin/bash

 source overlay_source.sh




ros2 run vision_stack image_publisher & ros2 run vision_stack line_tracking
