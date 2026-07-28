import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from std_msgs.msg import String
from sensor_msgs.msg import Image

import cv2
from cv_bridge import CvBridge
import numpy

import json, os, time


class EdgeRecog(Node):

    def __init__(self):
        super().__init__('edge_recog')
        self.subscription = self.create_subscription(
            Image,
            'green_mask',
            self.image_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.br = CvBridge()

        self.last_mtime = time.gmtime(0)
        self.config = self.load_config()

        # Hough Line Params
        self.rho = 1
        self.theta = numpy.pi / 180
        self.threshold = 15
        self.minLineLen = 50
        self.maxLineGap = 10



    def image_callback(self, msg):
        #Reload configs
        self.config = self.load_config()

        #Preprocess
        frame = self.br.imgmsg_to_cv2(msg,desired_encoding="bgr8")


        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray,(5, 5), 0)
        edges = cv2.Canny(blurred,50,150)

        #Detect
        lines = cv2.HoughLinesP(edges,self.rho,self.theta,self.threshold, minLineLength=self.minLineLen,maxLineGap = self.maxLineGap)

        #Draw lines
        if lines is not None:
            for line in lines:
                x1,y1,x2,y2 = line[0]
                cv2.line(frame, (x1,y1),(x2,y2), (0,255,0,), 2)
        
        cv2.imshow("edge_recog", frame)

        if cv2.waitKey(1) & 0xFF ==ord('q'):
            return 


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
            edge_recog = EdgeRecog()

            rclpy.spin(edge_recog)
            
            rclpy.shutdown()
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
