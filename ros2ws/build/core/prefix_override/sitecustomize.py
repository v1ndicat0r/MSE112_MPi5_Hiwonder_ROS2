import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/admin/MSE112_MPi5_Hiwonder_ROS2/ros2ws/install/core'
