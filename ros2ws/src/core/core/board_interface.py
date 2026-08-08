import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Int16MultiArray
from std_msgs.msg import ColorRGBA
from std_msgs.msg import Int16

import threading


class BoardInterface(Node):

    def __init__(self):
        super().__init__('board_interface')
        self.subscription = self.create_subscription(
            Int16,
            'sonar_topic',
            self.sonar_callback,
            10)
        self.subscription

        self.rgb1_publisher = self.create_publisher(ColorRGBA, 'rgb1_control', 10)
        self.rgb2_publisher = self.create_publisher(ColorRGBA, 'rgb2_control', 10)
        self.dc_motor_publisher = self.create_publisher(Int16MultiArray, 'dc_motor_control', 10)
        self.servo_publisher = self.create_publisher(Int16MultiArray, 'servo_control', 10)

        self.sonar = 0

        self.dc_motor_data = Int16MultiArray()
        self.dc_motor_data.data = [0,0,0,0]

    def sonar_callback(self,msg):
        self.sonar = msg.data

    def set_rgb1(self,r,g,b,a=1.0):
        rgba = ColorRGBA(r=r,g=g,b=b,a=a)
        self.rgb1_publisher.publish(rgba)

    def set_rgb2(self,r,g,b, a=1.0):
        rgba = ColorRGBA(r=r,g=g,b=b,a=a)
        self.rgb1_publisher.publish(rgba)

    def set_dc_motor_duty(self,motor_id,duty_cycle):
        self.dc_motor_data.data[motor_id-1] = duty_cycle
        self.dc_motor_publisher.publish(self.dc_motor_data)

        #Servo Limits
        #Servo6: 500 (Right 90)   -> 2500 (Left 90)
        #Servo5: 500 (Back 90)    -> 2500 (Forwards 90)
        #Servo4: 500 (Back 90)    -> 2500 (Forwards 90)
        #Servo3: 500 (Forward 90) -> 2500 (Back 90)
        #Servo1: 1550 (Closed)    -> 2400 (Open)

    def set_servo_position(self,servo_id,target):
        servo_data = Int16MultiArray()
        servo_data.data = [0,0,0,0,0,0]
        servo_data.data[servo_id-1] = target
        self.servo_publisher.publish(servo_data)

        #print(f'Setting servo %d to %d',servo_id, servo_data.data[servo_id-1])

    def set_servo_position_deg(self,servo_id,target):
        if servo_id == 6:
            if target > 90.0:
                target = 90.0
            if target < -90.0:
                target = -90.0
            self.set_servo_position(servo_id,int((-target+90.0)*2000.0/180.0+500.0))
        if servo_id == 5:
            if target < 0.0:
                target = 0.0
            if target > 180.0:
                target = 180.0
            self.set_servo_position(servo_id,int((180.0-target)*2000.0/180.0+500.0))
        if servo_id == 4:
            if target > 90.0:
                target = 90.0
            if target < -90.0:
                target = -90.0
            self.set_servo_position(servo_id,int((90.0-target)*2000.0/180.0+500.0))
        if servo_id == 3:
            if target > 90.0:
                target = 90.0
            if target < -90.0:
                target = -90.0
            self.set_servo_position(servo_id,int((target+90.0)*2000.0/180.0+500.0))
 
    def set_servo_position_rad(self,servo_id,target):
        self.set_servo_position_deg(servo_id,target*2*3.1415/360.0)

    def set_claw(self,state=0,s=''):
        servo_id = 1
        if s == '' :
            if state == 0:
                self.set_servo_position(servo_id,2400)
                return
            else:
                self.set_servo_position(servo_id,1550)
                return
        else:
            if s == 'open' or s == 'o' or s == 'opened':
                self.set_servo_position(servo_id,2400)
                return
            if s == 'close' or s == 'c' or s == 'closed':
                self.set_servo_position(servo_id,1550)
                return


def main() -> None:
    cucumber = 1
    #do nothing
    print('hello')


if __name__ == '__main__':
    main()
