#!/bin/bash

cd ..

source ./build_source.sh

rm -rf build install log

colcon build --symlink-install


