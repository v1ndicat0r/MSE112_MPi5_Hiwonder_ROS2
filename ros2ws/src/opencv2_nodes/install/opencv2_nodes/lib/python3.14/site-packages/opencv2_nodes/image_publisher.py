import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class ImagePublisher(Node):
    def __init__(self):
        super().__init__('image_publisher')
        self.publisher_ = self.create_publisher(Image, 'image_topic', 10)
        self.timer = self.create_timer(0.01, self.timer_callback)
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            raise RuntimeError("Could not open camera")

        self.br = CvBridge()
        self.display_status = 1

    def timer_callback(self):
        ret, frame = self.cap.read()
        if ret:
            #UNCOMMENT FOR BESPOKE IMAGE OUTPUT WINDOW
            #if self.display_status == 1:
                #cv2.imshow("camera", frame)

            #if cv2.waitKey(1) & 0xFF == ord('q'):
                #self.display_status = 0

            img_msg = self.br.cv2_to_imgmsg(frame, encoding="bgr8")
            self.publisher_.publish(img_msg)
        else:
            raise RuntimeError("Video capture failed")

def main(args=None):
    rclpy.init(args=args)
    image_publisher = ImagePublisher()
    rclpy.spin(image_publisher)
    image_publisher.cap.release()
    cv2.destroyAllWindows()
    rclpy.shutdown()

if __name__ == '__main__':
    main()