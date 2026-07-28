import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/public/ros2ws/src/opencv2_nodes/install/opencv2_nodes'
