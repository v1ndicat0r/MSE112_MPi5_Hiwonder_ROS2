# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from std_msgs.msg import String


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber_2')
        self.subscription = self.create_subscription(
            String,
            'whispoer',
            self.whisper1_callback,
            10)
        self.subscription = self.create_subscription(
            String,
            'whispoer2',
            self.whisper3_callback,
            10)
        self.subscription = self.create_subscription(
            String,
            'whispoer3',
            self.whisper2_callback,
            10)
        self.subscription  # prevent unused variable warning

    def whisper1_callback(self, msg):
    #whatever you want to do when hearing a whisper 1
        self.get_logger().info('I heard whisper 1: "%s"' % msg.data)
   
    def whisper2_callback(self, msg):
    #whatever you want to do when hearing a whisper 1
        self.get_logger().info('I heard w2: "%s"' % msg.data)
        
    def whisper3_callback(self, msg):
    #whatever you want to do when hearing a whisper 3
        self.get_logger().info('I heard w3: "%s"' % msg.data)


def main(args=None):
    try:
        with rclpy.init(args=args):
            minimal_subscriber = MinimalSubscriber()

            rclpy.spin(minimal_subscriber)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
