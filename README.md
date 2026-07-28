# Overview

To date this workspace contains 3 packages: 
  
*   hiwonder_board -> This package contains the drivers for the Hiwonder board
*   opencv2_nodes -> This package contains the various nodes that make up the opencv pipeline for line and object tracking (currently only green and blue lines functional)
*   controls_core -> This package is built around the main_control_node.py, in which the user's control scheme should be written
  
  
  # Running the stack
  
  Before running a build may be necessary. If you have determined that this is not needed, skip to the next step. To fully rebuild the workspace, go to /MSE112_MPi5_Hiwonder_ROS2/ros2ws/ and run the following command:
  
  	colcon build --symlink-install
  
   
  Next the install files must be sourced. Use the following command to source your terminal (still in the ros2ws directory). Remember this command for later, since every terminal you want to run a node in will require sourcing:
  
  	source overlay_source.sh
  
  To run the cv stack, use the provided bash file. Alternatively for running specific nodes to eliminate resource overusage go to the CV Stack section for a more detailed description:
  
  	./run_cv_pipeline.sh
  
  To run the main control node with the accompanying nodes for interfacing with the CV stack and the hiwonder board, open a new terminal window. Make sure to be in the ros2ws directory and remember to source it again. Then use the rollowing to run the nodes:
  
  	ros2 run controls_core main_control_node
Finally to run the hiwonder driver node open another new terminal in ros2ws and source it again, before running:

	ros2 run hiwonder_board hiwonder_board_node


# Building the Project

To fully build/reqbuild the entire project, navigate to the ros2ws directory and run the same command as previously:

	colcon build --symlink-install  

To only rebuild specific packages to cut down on buildtime use the following:

	colcon build --packages-select <your_package>



# Hiwonder Board Drivers
Notes to come

# OpenCV Stack

Notes to come

# Controls core

Notes to come


