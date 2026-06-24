#!/usr/bin/env python3
"""Publish alternating open/close commands for ZY gripper testing."""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


def clamp01(value):
    return max(0.0, min(1.0, float(value)))


class AutoTestPublisher(Node):
    def __init__(self):
        super().__init__('zy_gripper_auto_test')

        self.declare_parameter('open_position', 1.0)
        self.declare_parameter('close_position', 0.0)
        self.declare_parameter('flip_interval', 2.0)

        self.open_position = clamp01(
            self.get_parameter('open_position').get_parameter_value().double_value
        )
        self.close_position = clamp01(
            self.get_parameter('close_position').get_parameter_value().double_value
        )
        self.flip_interval = (
            self.get_parameter('flip_interval').get_parameter_value().double_value
        )
        if self.flip_interval <= 0.0:
            self.get_logger().warn('flip_interval must be > 0. Using 2.0 seconds.')
            self.flip_interval = 2.0

        self.left_publisher = self.create_publisher(
            Float32, '/control/gripperValueL', 10
        )
        self.right_publisher = self.create_publisher(
            Float32, '/control/gripperValueR', 10
        )

        self.is_open = True
        self.timer = self.create_timer(self.flip_interval, self.timer_callback)
        self.publish_position(self.open_position)

        self.get_logger().info(
            'ZY gripper auto test started. Publishing to /control/gripperValueL/R.'
        )

    def timer_callback(self):
        self.is_open = not self.is_open
        position = self.open_position if self.is_open else self.close_position
        self.publish_position(position)

    def publish_position(self, position):
        msg = Float32()
        msg.data = float(position)
        self.left_publisher.publish(msg)
        self.right_publisher.publish(msg)
        self.get_logger().info(f'Published gripper test position: {msg.data:.2f}')


def main(args=None):
    rclpy.init(args=args)
    node = AutoTestPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
