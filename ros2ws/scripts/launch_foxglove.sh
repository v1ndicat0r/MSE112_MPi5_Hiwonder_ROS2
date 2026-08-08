#!/usr/bin/env bash

cd ..

source ./overlay_source.sh

# Start the first process in the background
ros2 launch foxglove_bridge foxglove_bridge_launch.xml &

# Start the second process in the background
foxglove-studio &

# Wait for both processes to complete
wait

echo "Both processes have completed."

