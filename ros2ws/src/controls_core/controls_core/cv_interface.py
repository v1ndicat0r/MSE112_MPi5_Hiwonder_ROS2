import rclpy
from rclpy.node import Node
from std_msgs.msg import Int16MultiArray

import threading



class CVInterface(Node):

    def __init__(self):
        super().__init__('cv_interface')
        
        self.subscription = self.create_subscription(
            Int16MultiArray,
            'green_line_recog',
            self.green_line_callback,
            10)
        self.subscription = self.create_subscription(
            Int16MultiArray,
            'blue_line_recog',
            self.blue_line_callback,
            10)
        self.subscription  # prevent unused variable warning


        self.green_lines = (0,-240,0,240)
        self.blue_lines = (0,-240,0,240)
        

    def green_line_callback(self,msg):
        self.green_lines = (msg.data[0],-msg.data[1],msg.data[2],-msg.data[3])

    def blue_line_callback(self,msg):
        self.blue_lines = (msg.data[0],-msg.data[1],msg.data[2],-msg.data[3])

    def get_green_lines(self):
        return self.green_lines

    def get_blue_lines(self):
        return self.blue_lines




def main() -> None:
    cucumber = 1
    #do nothing
    print('hello')


if __name__ == '__main__':
    main()