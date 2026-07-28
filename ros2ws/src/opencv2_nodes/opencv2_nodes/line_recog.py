
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from std_msgs.msg import String
from sensor_msgs.msg import Image
from std_msgs.msg import Int16MultiArray

import cv2
from cv_bridge import CvBridge
import numpy

from ament_index_python.packages import get_package_share_directory
import json, os, time

from skimage.morphology import skeletonize
from skimage.util import invert
from skimage.util import img_as_ubyte

share_dir = get_package_share_directory("opencv2_nodes")
marker = "/install/"
idx = share_dir.find(marker)
WORKSPACE_PATH = share_dir[:idx] if idx != -1 else share_dir
CONFIG_PATH = f"{WORKSPACE_PATH}/src/opencv2_nodes/opencv2_nodes/configs.json"


class LineRecog(Node):

    def __init__(self):
        super().__init__('line_recog')
        self.subscription = self.create_subscription(
            Image,
            'green_mask',
            self.green_callback,
            10)
        self.subscription = self.create_subscription(
            Image,
            'blue_mask',
            self.blue_callback,
            10)
        self.subscription  # prevent unused variable warning

        self.green_publisher_visu = self.create_publisher(Image, 'green_line_recog_visu', 10)
        self.blue_publisher_visu = self.create_publisher(Image, 'blue_line_recog_visu', 10)
        self.green_publisher = self.create_publisher(Int16MultiArray, 'green_line_recog', 10)
        self.blue_publisher = self.create_publisher(Int16MultiArray, 'blue_line_recog', 10)


        self.br = CvBridge()

        self.last_mtime = time.gmtime(0)
        self.config = self.load_config()

        # Hough Line Params
        self.rho = 1
        self.theta = numpy.pi / 360
        self.threshold = 1
        self.minLineLen = 10
        self.maxLineGap = 10



    def green_callback(self, msg):
        #Reload configs
        self.config = self.load_config()

        #Preprocess
        binary = self.br.imgmsg_to_cv2(msg,desired_encoding="passthrough")

        # Clean noise
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)

        # Thicken and connect line segments
        kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        binary = cv2.dilate(binary, kernel2, iterations=2)
        

        #Skeletonize image and find lines
        skeleton = skeletonize(binary)
        lines = cv2.HoughLinesP(img_as_ubyte(skeleton),self.rho,self.theta,self.threshold, minLineLength=self.minLineLen,maxLineGap = self.maxLineGap)


        #Output visualization of lines
        out = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)

        if lines is not None:
            for line in lines:
                x1,y1,x2,y2 = line[0]
                cv2.line(out, (x1,y1),(x2,y2), (0,255,0,), 2)

        img_msg = self.br.cv2_to_imgmsg(out, encoding="passthrough")
        self.green_publisher_visu.publish(img_msg)

        #Output of line coordinates
        lines_out = Int16MultiArray()

        if lines is not None:
            for line in lines:
                x1,y1,x2,y2 = line[0]
                lines_out.data.extend([x1,y1,x2,y2])
        self.green_publisher.publish(lines_out)



    def blue_callback(self, msg):
        #Reload configs
        self.config = self.load_config()

        #Preprocess
        binary = self.br.imgmsg_to_cv2(msg,desired_encoding="passthrough")

        # Clean noise
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)

        # Thicken and connect line segments
        kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        binary = cv2.dilate(binary, kernel2, iterations=2)


        #Skeletonize image and find lines
        skeleton = skeletonize(binary)
        lines = cv2.HoughLinesP(img_as_ubyte(skeleton),self.rho,self.theta,self.threshold, minLineLength=self.minLineLen,maxLineGap = self.maxLineGap)

        #Output visualization of lines
        out = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)

        if lines is not None:
            for line in lines:
                x1,y1,x2,y2 = line[0]
                cv2.line(out, (x1,y1),(x2,y2), (0,255,0,), 2)
        
        img_msg = self.br.cv2_to_imgmsg(out, encoding="passthrough")
        self.blue_publisher_visu.publish(img_msg)

        #Output of line coordinates
        lines_out = Int16MultiArray()

        if lines is not None:
            for line in lines:
                x1,y1,x2,y2 = line[0]
                lines_out.data.extend([x1,y1,x2,y2])
        self.blue_publisher.publish(lines_out)


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
            line_recog = LineRecog()

            rclpy.spin(line_recog)
            
            rclpy.shutdown()
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
