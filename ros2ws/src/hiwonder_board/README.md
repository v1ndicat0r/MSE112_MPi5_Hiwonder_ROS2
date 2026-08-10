# Hiwonder board
This package contains the drivers for the serial communication to the Hiwonder breakout board, providing dc motor controls, servo controls and sonic feedback.

# Nodes
This package contains 1 node that can be run via command line execution:
* hiwonder_board_node

## Hiwonder_Board
This node performs 2 forms of serial communication:
* UART via ttyAMA0 to the Hiwonder board to control the servos, rgbs, dc motors, and buzzers.
* I2C to the sonar module (believed to be pass-through the Hiwonder board and header) (requires smbus2 module)


#### ros Information
This node publishes 1 topic:
* sonar_topic (Int16)

  Raw sonar sensor data is published with a period 150ms

This node is subscribed to 4 topics:

* dc_motor_control (Int16MultiArray)
  Sets the motors with id according to their array index (1 indexed) to the duty cycle described by their values in the array (-100 precent to 100 percent). Defaults to 0.
  
* servo_control (Int16MultiArray)
  Sets the servos with id according to their array index (1 indexed) to the position described by their values in the array. Values of 0 are ignored, allowing for simple distinguishing between whether to set a servo or not. Default values are hard coded to target the arm outstretched forwards (described at line 700 in the hiwonder_board_node.py file).

* rgb1_control (ColorRGBA)
  Sets the back RGB LED to the specified RGBA value
  
* rgb2_control (ColorRGBA)
  Sets the front RGB LED to the specified RGBA value
