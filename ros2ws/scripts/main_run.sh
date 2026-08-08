#!/bin/bash

cd ..

source ./overlay_source.sh

x-terminal-emulator -e bash -c "ros2 run core main;exec bash"
