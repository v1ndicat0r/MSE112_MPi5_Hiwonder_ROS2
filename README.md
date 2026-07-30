# Overview

To date this workspace contains 3 packages: 
  
*   hiwonder_board -> This package contains the drivers for the Hiwonder board
*   vision_stack -> This package contains the various nodes that make up the opencv pipeline for line and object tracking (currently only green and blue lines functional)
*   core -> This package is built around main.py, in which the user's control scheme should be written and all user facing coding takes place
  
  
  # Running the stack
  
  Before running a build may be necessary. If you have determined that this is not needed, skip to the next step. To fully rebuild the workspace, go to /MSE112_MPi5_Hiwonder_ROS2/ros2ws/ and run the following commands:
  
  	source build_source.sh
  	colcon build --symlink-install
  
   
  Next the install files must be sourced. Use the following command to source your terminal (still in the ros2ws directory). Remember this command for later, since every terminal you want to run a node in will require sourcing:
  
  	source overlay_source.sh
  
 
 To run all the nodes and executables use the run_all_with_terminals bash script (alternatively use run_all.sh to run without opening an extra terminal per process).
 	
 	./run_all_with_terminals.sh

 
 This may error out due to permission issues. In order to temporarily change your serial port's permissions run:
	
	sudo chmod 666 /dev/ttyAMA0
	
To prevent the kernel from resetting this at reboot, go to /etc/udev/rules.d and create a file called 99-tty-permissions.rules. In this paste the following:

	KERNEL=="ttyAMA0", MODE="0666"
	

# Building the Project

To fully build/reqbuild the entire project, navigate to the ros2ws directory and run the same command as previously:

	colcon build --symlink-install  

To only rebuild specific packages to cut down on buildtime use the following:

	colcon build --packages-select <your_package>


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
	ros2 run vision_stack bin_mask
	ros2 run vision_stack line_recog
	
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