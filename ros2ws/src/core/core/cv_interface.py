import rclpy
from rclpy.node import Node
from std_msgs.msg import Int16MultiArray
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from std_msgs.msg import String
from std_msgs.msg import Int16


import threading
import numpy as np



class CVInterface(Node):

    def __init__(self):
        super().__init__('cv_interface')
        self.image_subscription = self.create_subscription(
            Image,
            'image_topic',
            self.image_callback,
            10)
        self.image_subscription
        self.gmask_subscription = self.create_subscription(
            Image,
            'green_mask',
            self.green_callback,
            10)
        self.gmask_subscription
        self.bmask_subscription = self.create_subscription(
            Image,
            'blue_mask',
            self.blue_callback,
            10)
        self.bmask_subscription
        self.gline_subscription = self.create_subscription(
            Int16MultiArray,
            'green_line_recog',
            self.green_line_callback,
            10)
        self.gline_subscription
        self.bline_subscription = self.create_subscription(
            Int16MultiArray,
            'blue_line_recog',
            self.blue_line_callback,
            10)
        self.bline_subscription
        self.line_tracking_subscription = self.create_subscription(
            Int16,
            'line_tracking_topic',
            self.line_tracking_callback,
            10)
        self.line_tracking_subscription  # prevent unused variable warning

        self.target_line_color_publisher = self.create_publisher(String, 'target_line_color_topic', 10)


        self.br = CvBridge()


        h, w = 480, 640
        self.cam_image = np.zeros((h, w, 3), dtype=np.uint8)
       
        self.blue_mask = np.zeros((h, w), dtype=np.uint8)
        self.green_mask = np.zeros((h, w), dtype=np.uint8)

        self.green_line = (0,-240,0,240)
        self.blue_line = (0,-240,0,240)
        self.line_centroid_x = 0
        

    def green_line_callback(self,msg):
        self.green_lines = (msg.data[0],-msg.data[1],msg.data[2],-msg.data[3])

    def blue_line_callback(self,msg):
        self.blue_lines = (msg.data[0],-msg.data[1],msg.data[2],-msg.data[3])

    def green_callback(self,msg):
        self.green_mask = self.br.imgmsg_to_cv2(msg,desired_encoding="passthrough")
    
    def blue_callback(self,msg):
        self.blue_mask = self.br.imgmsg_to_cv2(msg,desired_encoding="passthrough")

    def image_callback(self,msg):
        self.cam_image = self.br.imgmsg_to_cv2(msg,desired_encoding="passthrough")

    def line_tracking_callback(self, msg):
        self.line_centroid_x = msg.data

    def set_target_line_color(self, target):
        msg = String()
        msg.data = target
        self.target_line_color_publisher.publish(msg)


def main() -> None:
    cucumber = 1
    #do nothing
    print('hello')


if __name__ == '__main__':
    main()