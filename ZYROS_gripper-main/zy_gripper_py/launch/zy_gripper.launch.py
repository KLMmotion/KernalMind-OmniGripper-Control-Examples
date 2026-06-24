#!/usr/bin/env python3
"""Launch file for zy_gripper_py OmniPicker motor node with configurable parameters."""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # Declare arguments (can be overridden via command line)
    vel_cmd_arg = DeclareLaunchArgument(
        'vel_cmd', default_value='100', description='Velocity command (0-100 percentage)')
    acc_cmd_arg = DeclareLaunchArgument(
        'acc_cmd', default_value='100', description='Acceleration command (0-100 percentage)')
    dec_cmd_arg = DeclareLaunchArgument(
        'dec_cmd', default_value='100', description='Deceleration command (0-100 percentage)')
    current_limit_arg = DeclareLaunchArgument(
        'current_limit', default_value='10000', description='Current/Force limit (10000 = 100% force)')
    
    auto_calibrate_arg = DeclareLaunchArgument(
        'auto_calibrate', default_value='false', description='Whether to auto calibrate min/max')
    
    m1_min_arg = DeclareLaunchArgument(
        'Motor1_min_pos', default_value='0.0', description='Manual min pos for Motor1 (if not auto)')
    m1_max_arg = DeclareLaunchArgument(
        'Motor1_max_pos', default_value='1.0', description='Manual max pos for Motor1 (if not auto)')
    m2_min_arg = DeclareLaunchArgument(
        'Motor2_min_pos', default_value='0.0', description='Manual min pos for Motor2 (if not auto)')
    m2_max_arg = DeclareLaunchArgument(
        'Motor2_max_pos', default_value='1.0', description='Manual max pos for Motor2 (if not auto)')

    left_motor_id_arg = DeclareLaunchArgument(
        'left_motor_id', default_value='8', description='CAN ID for left motor (default 8)')
    right_motor_id_arg = DeclareLaunchArgument(
        'right_motor_id', default_value='9', description='CAN ID for right motor (default 9)')

    node = Node(
        package='zy_gripper_py',
        executable='zy_gripper_node',  # 对应 setup.py 中配置的 entry_point
        name='omni_gripper_motor_node',
        output='screen',
        parameters=[{
            'vel_cmd': LaunchConfiguration('vel_cmd'),
            'acc_cmd': LaunchConfiguration('acc_cmd'),
            'dec_cmd': LaunchConfiguration('dec_cmd'),
            'current_limit': LaunchConfiguration('current_limit'),
            'auto_calibrate': LaunchConfiguration('auto_calibrate'),
            'Motor1_min_pos': LaunchConfiguration('Motor1_min_pos'),
            'Motor1_max_pos': LaunchConfiguration('Motor1_max_pos'),
            'Motor2_min_pos': LaunchConfiguration('Motor2_min_pos'),
            'Motor2_max_pos': LaunchConfiguration('Motor2_max_pos'),
            'left_motor_id': LaunchConfiguration('left_motor_id'),
            'right_motor_id': LaunchConfiguration('right_motor_id'),
        }]
    )

    return LaunchDescription([
        vel_cmd_arg,
        acc_cmd_arg,
        dec_cmd_arg,
        current_limit_arg,
        auto_calibrate_arg,
        m1_min_arg,
        m1_max_arg,
        m2_min_arg,
        m2_max_arg,
        left_motor_id_arg,
        right_motor_id_arg,
        node
    ])
