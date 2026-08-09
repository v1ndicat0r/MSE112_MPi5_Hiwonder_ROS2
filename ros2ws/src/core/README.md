
# Core
This package contains the main.py file used for the controls scheme, as well as the nodes that allow it to interface with the other packages.


# main.py

This file contains the place for the main control logic. Please stay within the designated comments.




# Nodes
This package starts 2 nodes when main is run:
* cv_interface
* board_interface

These handle the flow of data between the main file and the ros framework and provide an object oriented interface for the vision_stack and the hiwonder_booard to the main file. These nodes are callable in main using "cv" and "board".

## cv_interface
#### Functions
This node contains 6 attributes that should be accessed and 1 function to be called:
* line_centroid_x:

  	This attribute contains the live output from the line_tracking node and algorithm: pixel distance of the centroid of the detected line (line color defaults to green but can be set with the later mentioned set function. This value is to be used with project 1. 


* green_line:

	This attribute is updated on triggered recieve from the line_recog node and contains the start and end positions of the best fit green line in the form of a 4tuple
		
			green_line = (x1,y1,x2,y2)
	These values are given in cartesian coordinates, (0,0) is center screen and y,x are positive up, right. Defaults to a vertical line at x=0
* blue_line:
	
	This attribute is updated on triggered recieve from the line_recog node and contains the start and end positions of the recognized blue line in the form of a 4tuple
		
			blue_line = (x1,y1,x2,y2)
	These values are given in cartesian coordinates, (0,0) is center screen and y,x are positive up, right. Defaults to a vertical line at x=0

* cam_image:
		
	This attribute is updated on receive from the image_publisher and contains the full image captured by the camera in cv2 frame compatible data type (BGR-8 encoding).
	
* green_mask:
	
	This attribute is updated on receive from the bin_mask node and contains the green mask generated from the captured image. Returns a binary mask.

* blue_mask:
	
	This attribute is updated on receive from the bin_mask node and contains the green mask generated from the captured image. Returns a binary mask.

* set_target_line_color(target):

  	This function sets the target line color for the line tracking algorithm in line_tracking. This is done via the target_line_color_topic



#### ros Information
This node is subscribed to 6 topics:
* image_topic
* green_mask
* blue_mask
* green_line_recog
* blue_line_recog
* line_tracking_topic

This node publishes 1 topic:
* target_line_color_topic

## board_interface
### Functions
This node contains 1 attribute and 7 functions to access:
* sonar:
	
	This attribute contains the live ultrasonic sensor reading. Updates on receive. (Int16)
* set_rgb1(r,g,b, a=1.0):
	
	Sets the back rgb led to the specified values. Requires all floats as arguments.
	
* set_rgb2(r,g,b, a=1.0):

	Sets the front rgb led to the specified values. Requires all floats as arguments.
	
* set_dc_motor_duty(motor_id,duty_cycle):

	Sets the target DC Motor duty cycle. duty_cycle is an integer between -100 and 100 describing directional percent
	
* set_servo_position(servo_id,target):
	
	Sets the selected servo to the raw target position. The range of target values are generally 500-2500.
	
* set_servo_position_deg(servo_id,target):

	Sets the selected servo to the target position described in degrees. 0 position is with the arm fully outstretched to the front. This may be unit specific depending on servo installation.
	
* set_servo_posiiton_rad(servo_id, target):

	Sets the selected servo to the target position described in radians. 0 position is with the arm fully outstretched to the front. This may be unit specific depending on servo installation.
	
* set_claw(state):

	Sets the claw to either the open position or the closed position, determined by state = 0 or 1 (respectively). Alternative form set_claw(s='open') or set_claw(s='close'). This may be unit specific depending on servo installation.
	
	
#### ros Information
This node is subscribed to 1 topic:
* sonar_topic (Int16)

This node publishes to 4 topics:
* rgb1_control (ColorRGBA)
* rgb2_control (ColorRGBA)
* dc_motor_control (Int16MultiArray)
* servo_control (Int16MultiArray)
