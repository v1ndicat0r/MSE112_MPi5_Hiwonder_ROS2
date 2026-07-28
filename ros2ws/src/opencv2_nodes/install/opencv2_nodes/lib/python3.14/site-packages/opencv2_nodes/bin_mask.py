import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from std_msgs.msg import String
from sensor_msgs.msg import Image


import cv2
from cv_bridge import CvBridge
import numpy

import json, time, os

CONFIG_PATH = "configs.json"

class BinMask(Node):

    def __init__(self):
        super().__init__('bin_mask')
        self.subscription = self.create_subscription(
            Image,
            'image_topic',
            self.image_callback,
            10)
        self.subscription  # prevent unused variable warning

        self.green_publisher = self.create_publisher(Image, 'green_mask', 10)
        self.blue_publisher = self.create_publisher(Image, 'blue_mask', 10)

        self.br = CvBridge()

        #Load initial params
        self.last_mtime = time.gmtime(0)
        self.config = self.load_config()
        



    def image_callback(self, msg):
        #Reload config
        self.load_config()
        green_lower = numpy.array([self.config("green_h_min_init",0),self.config("green_s_min_init",0),self.config("green_v_min_init",0)])
        green_upper = numpy.array([self.config("green_h_max_init",255),self.config("green_s_max_init",255),self.config("green_v_max_init",255)])
            
            
        
        #Preprocess
        frame = self.br.imgmsg_to_cv2(msg,desired_encoding="bgr8")
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        blurred = cv2.GaussianBlur(hsv,(4, 4), 0)


        #Apply green mask
        green_masked = cv2.inRange(blurred,green_lower,green_upper)


        #Apply blue mask


        #Publish mask
        img_msg = self.br.cv2_to_imgmsg(frame, encoding="bgr8")
        self.publisher_.publish(img_msg)



    def load_config(self,path=CONFIG_PATH):
        mtime = get_mtime(JSON_PATH)
        if mtime != self.last_mtime:
            params = load_params(JSON_PATH)
            self.last_mtime = mtime
        
            with open(path, "r", encoding="utf-8") as f:
                self.config = json.load(f)

def main(args=None):
    try:
        with rclpy.init(args=args):
            bin_mask = BinMask()

            rclpy.spin(bin_mask)
            
            rclpy.shutdown()
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
