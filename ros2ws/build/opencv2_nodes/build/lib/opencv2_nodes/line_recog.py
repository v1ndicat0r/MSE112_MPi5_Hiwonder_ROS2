
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from std_msgs.msg import String
from sensor_msgs.msg import Image
from std_msgs.msg import Int16MultiArray

import cv2
from cv_bridge import CvBridge
import numpy
import math

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
        self.threshold = 2
        self.minLineLen = 20
        self.maxLineGap = 5

        #Hold best fit lines
        self.x1_bestfit_green = 0
        self.y1_bestfit_green = -240
        self.x2_bestfit_green = 0
        self.y2_bestfit_green = 240

        self.x1_bestfit_blue = 0
        self.y1_bestfit_blue = -240
        self.x2_bestfit_blue = 0
        self.y2_bestfit_blue = 240





    def green_callback(self, msg):
        #Reload configs
        self.config = self.load_config()

        #Reormat for cv
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

        #Output for building debug visualization
        out = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)

        #Iterate through segments to find the line length weighted centroid, average slope, and min/max y vals
        x_avg = 0
        y_avg = 0
        slope_avg = 480
        y_max = -240
        y_min = 240
        line_counter = 0
        total_lines_len = 0

        if lines is not None:
            for line in lines:
                x1,y1,x2,y2 = line[0]

                #Draw line segments for debug
                cv2.line(out, (x1,y1),(x2,y2), (0,255,0,), 2)

                #Ensure the slope is in the correct direction
                if x1>x2:
                    temp = x1
                    x1=x2
                    x2=temp
                    temp = y1
                    y1 = y2
                    y2 = temp

                #Track min/max y values
                if y1-240>y_max:
                    y_max = y1-240
                if y2-240>y_max:
                    y_max = y2-240
                if y1-240<y_min:
                    y_min = y1-240
                if y2-240<y_min:
                    y_min = y2-240


                #Find segment length and track total segmant length
                line_len = math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))
                total_lines_len += line_len

                #Track lines processed
                line_counter += 1

                #Accumulate coordinates weighted based on segment length
                x_avg += (x1-320 + x2-320)*line_len/2
                y_avg += (y1-240 + y2-240)*line_len/2

                #Adjust slope average
                if x1==x2:
                    m = 480.0
                else:
                    m = (y2-y1)/(x2-x1)
                slope_avg = (slope_avg * (line_counter-1) + m)/line_counter
                
                print(f"Processing line: {line_counter} \r\n    Slope: {m}\r\n    Start: {x1-320}, {y1-240}\r\n    End: {x2-320}, {y2-240}\r\n    Length: {line_len}")
            
            #Average out the coordinates according to accumulated length
            x_avg = x_avg/total_lines_len
            y_avg = y_avg/total_lines_len
            print(f"\r\n\r\nIteration complete:\r\n     x_avg: {x_avg}\r\n    y_avg: {y_avg}\r\n    Slope: {slope_avg}\r\n\r\n")

        else:
            print("No Lines")
  
        print(f"Line count: {line_counter}")
        
        #Ensure slope non-zero predivision
        if slope_avg == 0.0:
            slope_avg = 1.0

        #Convert centroid and slope to line coordinates using min/max y vals as end points
        #slope y = mx + b
        # b = y - mx 
        # x  = (y - b)/m
        avg_offset = y_avg - slope_avg * x_avg
        self.x1_bestfit_green = int((y_min - avg_offset) / slope_avg)
        self.y1_bestfit_green = int(y_min)
        self.x2_bestfit_green = int((y_max - avg_offset) / slope_avg)
        self.y2_bestfit_green = int(y_max)        

        
        
        #Draw best fit line for debug
        cv2.line(out, (self.x1_bestfit_green+320,self.y1_bestfit_green+240),(self.x2_bestfit_green+320,self.y2_bestfit_green+240), (255,0,0,), 10)

        #Publish debug image
        img_msg = self.br.cv2_to_imgmsg(out, encoding="passthrough")
        self.green_publisher_visu.publish(img_msg)

        #Publish line coordinates
        lines_out = Int16MultiArray()

        lines_out.data.extend([self.x1_bestfit_green,self.y1_bestfit_green,self.x2_bestfit_green,self.y2_bestfit_green])
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



        #Iterate through segments to find the line length weighted centroid, average slope, and min/max y vals
        x_avg = 0
        y_avg = 0
        slope_avg = 480
        y_max = -240
        y_min = 240
        line_counter = 0
        total_lines_len = 0

        if lines is not None:
            for line in lines:
                x1,y1,x2,y2 = line[0]

                #Draw line segments for debug
                cv2.line(out, (x1,y1),(x2,y2), (0,255,0,), 2)

                #Ensure the slope is in the correct direction
                if x1>x2:
                    temp = x1
                    x1=x2
                    x2=temp
                    temp = y1
                    y1 = y2
                    y2 = temp

                #Track min/max y values
                if y1-240>y_max:
                    y_max = y1-240
                if y2-240>y_max:
                    y_max = y2-240
                if y1-240<y_min:
                    y_min = y1-240
                if y2-240<y_min:
                    y_min = y2-240


                #Find segment length and track total segmant length
                line_len = math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))
                total_lines_len += line_len

                #Track lines processed
                line_counter += 1

                #Accumulate coordinates weighted based on segment length
                x_avg += (x1-320 + x2-320)*line_len/2
                y_avg += (y1-240 + y2-240)*line_len/2

                #Adjust slope average
                if x1==x2:
                    m = 480.0
                else:
                    m = (y2-y1)/(x2-x1)
                slope_avg = (slope_avg * (line_counter-1) + m)/line_counter
                
                print(f"Processing line: {line_counter} \r\n    Slope: {m}\r\n    Start: {x1-320}, {y1-240}\r\n    End: {x2-320}, {y2-240}\r\n    Length: {line_len}")
            
            #Average out the coordinates according to accumulated length
            x_avg = x_avg/total_lines_len
            y_avg = y_avg/total_lines_len
            print(f"\r\n\r\nIteration complete:\r\n     x_avg: {x_avg}\r\n    y_avg: {y_avg}\r\n    Slope: {slope_avg}\r\n\r\n")

        else:
            print("No Lines")
  
        print(f"Line count: {line_counter}")
        
        #Ensure slope non-zero predivision
        if slope_avg == 0.0:
            slope_avg = 1.0

        #Convert centroid and slope to line coordinates using min/max y vals as end points
        #slope y = mx + b
        # b = y - mx 
        # x  = (y - b)/m
        avg_offset = y_avg - slope_avg * x_avg
        self.x1_bestfit_blue = int((y_min - avg_offset) / slope_avg)
        self.y1_bestfit_blue = int(y_min)
        self.x2_bestfit_blue = int((y_max - avg_offset) / slope_avg)
        self.y2_bestfit_blue = int(y_max)        

        
        
        #Draw best fit line for debug
        cv2.line(out, (self.x1_bestfit_blue+320,self.y1_bestfit_blue+240),(self.x2_bestfit_blue+320,self.y2_bestfit_blue+240), (255,0,0,), 10)


        #Publish debug visualization
        img_msg = self.br.cv2_to_imgmsg(out, encoding="passthrough")
        self.blue_publisher_visu.publish(img_msg)

        #Output of line coordinates
        lines_out = Int16MultiArray()

        lines_out.data.extend([self.x1_bestfit_blue,self.y1_bestfit_blue,self.x2_bestfit_blue,self.y2_bestfit_blue])
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
