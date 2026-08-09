# Overview

To date this workspace contains 3 packages: 
  
*   hiwonder_board -> This package contains the driver node for the Hiwonder board
*   vision_stack -> This package contains the various nodes that make up the opencv pipeline for line and object tracking
*   core -> This package is built around main.py, in which the user's control scheme should be written and all user facing coding takes place

  
# Setup
  
  In order to use this workspace, some dependancies will have to be installed. 
  First, ensure ROS2 Lyrical Luth is installed on the system.
  Next go to /MSE112_MPi5_Hiwonder_ROS2/ . In here you will find two setup scripts. Run the first one, then you will be prompted to reboot. After this reboot run the second, and all dependancies will be installed, and udev rules will be edited to make the required devices accessible.

  
  # Running the stack
  
  Before running a build may be necessary. If you have determined that this is not needed, skip to the next step. To fully rebuild the workspace, go to /MSE112_MPi5_Hiwonder_ROS2/ros2ws/scripts and run the following script:
  
  	./force_full_rebuild.sh
  
 
 To run all the nodes and executables needed for project 1: line tracking, use the proj1_run.sh bash script:
 	
 	./proj1_run.sh



# Building the Project

To fully build/rebuild the entire project, navigate to the ros2ws directory and run the same command as previously:

	colcon build --symlink-install  

To only rebuild specific packages to cut down on buildtime use the following:

	colcon build --packages-select <your_package>

These actions can now also be performed simply by navigating to /ros2ws/scripts and running the according script.


# Core

To run the main.py file with the accompanying nodes for interfacing with the CV stack and the hiwonder board, open a new terminal window and source it. 

	source overlay_source.sh
	
Make sure to be in the ros2ws directory, then use the rollowing to run the program:
  
  	ros2 run core main

For more details, see the README file in /ros2ws/src/core/

# Hiwonder Board Drivers
To run the hiwonder driver node open another new terminal in ros2ws and source it again, before running the main node:

	source overlay_source.sh
	ros2 run hiwonder_board hiwonder_board_node


For more details, see the README file in /ros2ws/src/hiwonder_board/

# Vision Stack

To run the cv stack, use the provided bash file:
  
  	./run_cv_stack.sh

Alternatively for running specific nodes to eliminate resource overusage select one of the following:

	ros2 run vision_stack image_publisher 
	ros2 run vision_stack line_tracking
	
To tune the binary mask, the configs.json file located in /ros2ws/src/vision_stack/vision_stack/ contains the threshold values for the binary mask and can be updated during runtime.

For more details, see the README file in /ros2ws/src/vision_stack/

# Foxglove
A good tool for monitoring the active topics (especially for vision visualizations) is Foxglove. 

To install this, navigate to the /foxglove_installation directory in the github repository root directory (or visit their site to install) and run the following to install the app and the ros bridge:

	sudo apt install ./foxglove-studio-*.deb	 
	sudo apt install ros-$ROS_DISTRO-foxglove-bridge
	
It can now be easily run from the ros2ws directory with:

	./launch_foxglove.sh
	
To access your bridge navigate to "Open connection" in the dashboard. Then click "Open" making sure "Foxglove Websocket" is selected.
