#!/bin/bash

cd ..

source build_source.sh

colcon build --packages-select core

