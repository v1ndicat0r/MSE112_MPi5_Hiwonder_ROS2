import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from std_msgs.msg import String
from sensor_msgs.msg import Image


import cv2
from cv_bridge import CvBridge
import numpy

import json, time, os

from ament_index_python.packages import get_package_share_directory


share_dir = get_package_share_directory("vision_stack")
marker = "/install/"
idx = share_dir.find(marker)
WORKSPACE_PATH = share_dir[:idx] if idx != -1 else share_dir
CONFIG_PATH = f"{WORKSPACE_PATH}/src/vision_stack/vision_stack/configs.json"


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
        self.config = self.load_config()

        green_lower = numpy.array([self.config.get("green_h_min_init",0),self.config.get("green_s_min_init",0),self.config.get("green_v_min_init",0)])
        green_upper = numpy.array([self.config.get("green_h_max_init",255),self.config.get("green_s_max_init",255),self.config.get("green_v_max_init",255)])

        blue_lower = numpy.array([self.config.get("blue_h_min_init",0),self.config.get("blue_s_min_init",0),self.config.get("blue_v_min_init",0)])
        blue_upper = numpy.array([self.config.get("blue_h_max_init",255),self.config.get("blue_s_max_init",255),self.config.get("blue_v_max_init",255)])
        
        #Preprocess
        frame = self.br.imgmsg_to_cv2(msg,desired_encoding="bgr8")
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        blurred = cv2.GaussianBlur(hsv,(9, 9), 0)

        #Apply green mask
        green_mask = cv2.inRange(blurred,green_lower,green_upper)
        green_masked = cv2.bitwise_and(frame, frame, mask=green_mask)

        #Apply blue mask
        blue_mask = cv2.inRange(blurred,blue_lower,blue_upper)
        blue_masked = cv2.bitwise_and(frame, frame, mask=blue_mask)

        #Publish mask
        img_msg = self.br.cv2_to_imgmsg(green_mask, encoding="passthrough")
        self.green_publisher.publish(img_msg)

        img_msg = self.br.cv2_to_imgmsg(blue_mask, encoding="passthrough")
        self.blue_publisher.publish(img_msg)


    def load_config(self,path=CONFIG_PATH):
        mtime = os.path.getmtime(path)
        if mtime != self.last_mtime:
            self.last_mtime = mtime
            
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return self.config



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
