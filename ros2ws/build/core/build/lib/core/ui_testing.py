#!/usr/bin/env python3

import sys

import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64MultiArray, Empty, Bool
from sensor_msgs.msg import JointState

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QHBoxLayout,
    QDoubleSpinBox,
    QGroupBox,
)

from PyQt5.QtCore import Qt, QTimer


class RobotGUI(Node):

    def __init__(self):

        super().__init__("robot_arm_gui")

        self.publisher = self.create_publisher(
            Float64MultiArray,
            "/arm/joint_position_cmd",
            10
        )

        self.stop_pub = self.create_publisher(
            Bool,
            "/arm/stop",
            10
        )

        self.home_pub = self.create_publisher(
            Empty,
            "/arm/home",
            10
        )

        self.subscription = self.create_subscription(
            JointState,
            "/joint_states",
            self.joint_callback,
            10
        )

        self.current_positions = [0.0, 0.0, 0.0, 0.0]

    def joint_callback(self, msg):

        if len(msg.position) >= 4:
            self.current_positions = list(msg.position[:4])


class MainWindow(QWidget):

    def __init__(self, node):

        super().__init__()

        self.node = node

        self.setWindowTitle("ROS2 4DOF Robot Controller")

        self.joints = [0.0] * 4

        self.sliders = []
        self.spinboxes = []
        self.feedback = []

        layout = QVBoxLayout()

        group = QGroupBox("Joint Control")

        group_layout = QVBoxLayout()

        for i in range(4):

            row = QHBoxLayout()

            label = QLabel(f"Joint {i+1}")

            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(-180)
            slider.setMaximum(180)
            slider.setValue(0)

            spin = QDoubleSpinBox()
            spin.setRange(-180, 180)
            spin.setDecimals(1)
            spin.setSingleStep(1)

            feedback = QLabel("Current: 0.0°")

            slider.valueChanged.connect(
                lambda value, j=i: self.slider_changed(j, value)
            )

            spin.valueChanged.connect(
                lambda value, j=i: self.spin_changed(j, value)
            )

            row.addWidget(label)
            row.addWidget(slider)
            row.addWidget(spin)
            row.addWidget(feedback)

            group_layout.addLayout(row)

            self.sliders.append(slider)
            self.spinboxes.append(spin)
            self.feedback.append(feedback)

        group.setLayout(group_layout)

        layout.addWidget(group)

        home_button = QPushButton("Home")
        stop_button = QPushButton("Emergency Stop")

        home_button.clicked.connect(self.home)
        stop_button.clicked.connect(self.stop)

        layout.addWidget(home_button)
        layout.addWidget(stop_button)

        self.setLayout(layout)

        self.feedback_timer = QTimer()
        self.feedback_timer.timeout.connect(self.update_feedback)
        self.feedback_timer.start(100)

    def slider_changed(self, joint, value):

        self.spinboxes[joint].blockSignals(True)
        self.spinboxes[joint].setValue(value)
        self.spinboxes[joint].blockSignals(False)

        self.joints[joint] = float(value)

        self.publish()

    def spin_changed(self, joint, value):

        self.sliders[joint].blockSignals(True)
        self.sliders[joint].setValue(int(value))
        self.sliders[joint].blockSignals(False)

        self.joints[joint] = value

        self.publish()

    def publish(self):

        msg = Float64MultiArray()

        msg.data = self.joints

        self.node.publisher.publish(msg)

    def home(self):

        for slider in self.sliders:
            slider.setValue(0)

        self.node.home_pub.publish(Empty())

    def stop(self):

        msg = Bool()

        msg.data = True

        self.node.stop_pub.publish(msg)

    def update_feedback(self):

        for i in range(4):

            angle = self.node.current_positions[i]

            self.feedback[i].setText(
                f"Current: {angle:.2f}°"
            )


def main():

    rclpy.init()

    node = RobotGUI()

    app = QApplication(sys.argv)

    window = MainWindow(node)

    window.show()

    timer = QTimer()
    timer.timeout.connect(lambda: rclpy.spin_once(node, timeout_sec=0.0))
    timer.start(10)

    app.exec()

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()
