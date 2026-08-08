import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Image
from std_msgs.msg import Int16
import cv2
from cv_bridge import CvBridge
import numpy
import numpy as np
import math
import json, time, os
from ament_index_python.packages import get_package_share_directory

# Get path to config file
share_dir = get_package_share_directory("vision_stack")
marker = "/install/"
idx = share_dir.find(marker)
WORKSPACE_PATH = share_dir[:idx] if idx != -1 else share_dir
CONFIG_PATH = f"{WORKSPACE_PATH}/src/vision_stack/vision_stack/configs.json"


class LineTracking(Node):

    def __init__(self):
        super().__init__('line_tracking')
        self.subscription = self.create_subscription(
            Image,
            'image_topic',
            self.image_callback,
            10)
        self.subscription = self.create_subscription(
            String,
            'target_line_color_topic',
            self.set_target_color,
            10)
        self.subscription  # prevent unused variable warning

        self.line_publisher = self.create_publisher(Int16, 'line_tracking_topic', 10)

        self.br = CvBridge()

        #Load initial params
        self.last_mtime = time.gmtime(0)
        self.config = self.load_config()

    # Line tracking imported initializations

        # line tracking
        self.__target_color = ('green')
        
        self.roi = [ # [ROI, weight]
                (240, 280,  0, 640, 0.1), 
                (340, 380,  0, 640, 0.3), 
                (430, 460,  0, 640, 0.6)
            ]

        self.roi_h1 = self.roi[0][0]
        self.roi_h2 = self.roi[1][0] - self.roi[0][0]
        self.roi_h3 = self.roi[2][0] - self.roi[1][0]

        self.roi_h_list = [self.roi_h1, self.roi_h2, self.roi_h3]
        self.size = (640, 480)
        self.img_centerx = 320

        self.line_centerx = 0
        

    # Find the contour with the largest area
    # The parameter is a list of contours to be compared
    def getAreaMaxContour(self,contours):
        contour_area_temp = 0
        contour_area_max = 0
        area_max_contour = None

        for c in contours:  # Iterate over all contours
            contour_area_temp = math.fabs(cv2.contourArea(c))  # Calculate the contour area
            if contour_area_temp > contour_area_max:
                contour_area_max = contour_area_temp
                if contour_area_temp >= 5:  # Only when the area is greater than 300, the contour of the largest area is valid to filter out interference
                    area_max_contour = c

        return area_max_contour, contour_area_max  # Return the largest contour

    def map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


    def set_target_color(self, msg):
        self.__target_color = msg.data


    def image_callback(self, msg):

        #Convert ros msg to cv2 img
        img = self.br.imgmsg_to_cv2(msg,desired_encoding="bgr8")
        img_copy = img.copy()
        img_h, img_w = img.shape[:2]


        #Reload binary masking configs
        self.config = self.load_config()

        green_lower = numpy.array([self.config.get("green_h_min_init",0),self.config.get("green_s_min_init",0),self.config.get("green_v_min_init",0)])
        green_upper = numpy.array([self.config.get("green_h_max_init",255),self.config.get("green_s_max_init",255),self.config.get("green_v_max_init",255)])

        blue_lower = numpy.array([self.config.get("blue_h_min_init",0),self.config.get("blue_s_min_init",0),self.config.get("blue_v_min_init",0)])
        blue_upper = numpy.array([self.config.get("blue_h_max_init",255),self.config.get("blue_s_max_init",255),self.config.get("blue_v_max_init",255)])

        red_lower = numpy.array([self.config.get("red_h_min_init",0),self.config.get("red_s_min_init",0),self.config.get("red_v_min_init",0)])
        red_upper = numpy.array([self.config.get("red_h_max_init",255),self.config.get("red_s_max_init",255),self.config.get("red_v_max_init",255)])


        # Line tracking inits
        frame_resize = cv2.resize(img_copy, self.size, interpolation=cv2.INTER_NEAREST)
        frame_gb = cv2.GaussianBlur(frame_resize, (3, 3), 3)         
        centroid_x_sum = 0
        weight_sum = 0
        center_ = []
        n = 0


        # Split the image into three parts: upper, middle and lower. This will make the processing faster and more accurate.
        for r in self.roi:
            roi_h = self.roi_h_list[n]
            n += 1       
            blobs = frame_gb[r[0]:r[1], r[2]:r[3]]
            hsv = cv2.cvtColor(frame_gb, cv2.COLOR_BGR2HSV)  # Convert the image to HSV space
            area_max = 0
            areaMaxContour = 0

            
            if self.__target_color == 'green':
                frame_mask = cv2.inRange(hsv,green_lower,green_upper)
            elif self.__target_color == 'blue':
                frame_mask = cv2.inRange(hsv,blue_lower,blue_upper)
            elif self.__target_color == 'red':
                frame_mask = cv2.inRange(hsv,red_lower,red_upper)
            else:
                frame_mask = np.zeros(frame_resize.shape[:2],dtype=np.uint8)


            eroded = cv2.dilate(frame_mask, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)),iterations=7)  #corrosion
            dilated = cv2.erode(eroded, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)),iterations=7) #Expansion
            tophat = blackhat = cv2.morphologyEx(dilated, cv2.MORPH_TOPHAT, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))  #tophat


            cnts = cv2.findContours(dilated , cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)[-2]# Find all contours
            cnt_large, area = self.getAreaMaxContour(cnts)# Find the contour with the largest area
            if cnt_large is not None:#If the contour is not empty
                
                rect = cv2.minAreaRect(cnt_large)#Minimum enclosing rectangle
                
                box = cv2.boxPoints(rect)#The four vertices of the minimum enclosing rectangle
                box = box.astype(np.int32)

                for i in range(4):
                    box[i, 1] = box[i, 1] + (n - 1)*roi_h + self.roi[0][0]
                    box[i, 1] = int(self.map(box[i, 1], 0, self.size[1], 0, img_h))
                for i in range(4):                
                    box[i, 0] = int(self.map(box[i, 0], 0, self.size[0], 0, img_w))
                try:
                    cv2.drawContours(img, [box], -1, (0,0,255,255), 2)#Draw a rectangle consisting of four points
                    cv2.drawContours(img, cnts, -1, (0,0,255,255), 2)
                except:
                    cucumber = 1
                #Get the diagonal points of the rectangle
                pt1_x, pt1_y = box[0, 0], box[0, 1]
                pt3_x, pt3_y = box[2, 0], box[2, 1]            
                center_x, center_y = (pt1_x + pt3_x) / 2, (pt1_y + pt3_y) / 2#Center point       
                cv2.circle(img, (int(center_x), int(center_y)), 5, (0,0,255), -1)# Draw the center point         
                center_.append([center_x, center_y])                        
                #Sum the top, middle and bottom center points according to different weights
                centroid_x_sum += center_x * r[4]
                weight_sum += r[4]
        if weight_sum != 0:
            #Find the final center point
            self.line_centerx = int(centroid_x_sum / weight_sum)-self.img_centerx
            cv2.circle(img, (self.line_centerx, int(center_y)), 20, (0,255,255), -1)# Draw the center point
        else:
            self.line_centerx = 0
        
        msg_out = Int16()
        msg_out.data = self.line_centerx
        self.line_publisher.publish(msg_out)

        #cv2.imshow("line_tracking", dilated)
        #cv2.waitKey(1)


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
            line_tracking = LineTracking()

            rclpy.spin(line_tracking)
            
            rclpy.shutdown()
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
