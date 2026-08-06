import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
import numpy
import numpy as np
import json, time, os
from ament_index_python.packages import get_package_share_directory

# Get path to config file
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

    # Line tracking imported initializations

        # line tracking
        self.__target_color
        
        self.roi = [ # [ROI, weight]
                (240, 280,  0, 640, 0.1), 
                (340, 380,  0, 640, 0.3), 
                (430, 460,  0, 640, 0.6)
            ]

        self.roi_h1 = roi[0][0]
        self.roi_h2 = roi[1][0] - roi[0][0]
        self.roi_h3 = roi[2][0] - roi[1][0]

        self.roi_h_list = [roi_h1, roi_h2, roi_h3]
        self.size = (640, 480)
        self.img_centerx = 320

        self.line_centerx = 0
        

    # Find the contour with the largest area
    # The parameter is a list of contours to be compared
    def getAreaMaxContour(contours):
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



    def image_callback(self, msg):

        #Convert rtos msg to cv2 img
        img = self.br.imgmsg_to_cv2(msg,desired_encoding="bgr8")
        img_copy = img.copy()
        img_h, img_w = img.shape[:2]


        #Reload binary masking configs
        self.config = self.load_config()

        green_lower = numpy.array([self.config.get("green_h_min_init",0),self.config.get("green_s_min_init",0),self.config.get("green_v_min_init",0)])
        green_upper = numpy.array([self.config.get("green_h_max_init",255),self.config.get("green_s_max_init",255),self.config.get("green_v_max_init",255)])

        blue_lower = numpy.array([self.config.get("blue_h_min_init",0),self.config.get("blue_s_min_init",0),self.config.get("blue_v_min_init",0)])
        blue_upper = numpy.array([self.config.get("blue_h_max_init",255),self.config.get("blue_s_max_init",255),self.config.get("blue_v_max_init",255)])
        


        # Line tracking inits
        frame_resize = cv2.resize(img_copy, size, interpolation=cv2.INTER_NEAREST)
        frame_gb = cv2.GaussianBlur(frame_resize, (3, 3), 3)         
        centroid_x_sum = 0
        weight_sum = 0
        center_ = []
        n = 0


        # Split the image into three parts: upper, middle and lower. This will make the processing faster and more accurate.
        for r in roi:
            roi_h = roi_h_list[n]
            n += 1       
            blobs = frame_gb[r[0]:r[1], r[2]:r[3]]
            frame_lab = cv2.cvtColor(blobs, cv2.COLOR_BGR2LAB)  # Convert the image to LAB space
            area_max = 0
            areaMaxContour = 0
            for i in lab_data:
                if i in __target_color:
                    detect_color = i

                    # TODO create frame mask using cv2.inRange () function to perform bitwise operations on the original image

                    # /.....enter code here...../

                    eroded = cv2.erode(frame_mask, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))  #corrosion
                    dilated = cv2.dilate(eroded, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))) #Expansion

            cnts = cv2.findContours(dilated , cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)[-2]# Find all contours
            cnt_large, area = self.getAreaMaxContour(cnts)# Find the contour with the largest area
            if cnt_large is not None:#If the contour is not empty
                rect = cv2.minAreaRect(cnt_large)#Minimum enclosing rectangle
                box = np.int0(cv2.boxPoints(rect))#The four vertices of the minimum enclosing rectangle
                for i in range(4):
                    box[i, 1] = box[i, 1] + (n - 1)*roi_h + roi[0][0]
                    box[i, 1] = int(Misc.map(box[i, 1], 0, size[1], 0, img_h))
                for i in range(4):                
                    box[i, 0] = int(Misc.map(box[i, 0], 0, size[0], 0, img_w))

                cv2.drawContours(img, [box], -1, (0,0,255,255), 2)#Draw a rectangle consisting of four points
            
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
            line_centerx = int(centroid_x_sum / weight_sum)
            cv2.circle(img, (line_centerx, int(center_y)), 10, (0,255,255), -1)# Draw the center point
        else:
            line_centerx = -1
        return img

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
