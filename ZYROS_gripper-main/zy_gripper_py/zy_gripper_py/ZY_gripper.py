"""ROS2 智元 OmniPicker 夹爪独立控制节点"""

import time
import numpy as np

try:
    from .ZY_CAN import OmniMotor, ZYMotorControl
except ImportError:
    from ZY_CAN import OmniMotor, ZYMotorControl

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, Float32MultiArray, Int32MultiArray
from std_srvs.srv import Trigger

# 全局变量
Motor1, Motor2, ZYCtrl = None, None, None
Motor1_min_pos, Motor1_max_pos = 0.0, 1.0
Motor2_min_pos, Motor2_max_pos = 0.0, 1.0
auto_calibrate = False


class OmniGripperNode(Node):
    def __init__(self):
        super().__init__('omni_gripper_motor_node')

        self.declare_parameter('current_limit', 10000)
        self.declare_parameter('vel_cmd', 100)
        self.declare_parameter('acc_cmd', 100)
        self.declare_parameter('dec_cmd', 100)

        self.declare_parameter('auto_calibrate', False)
        self.declare_parameter('Motor1_min_pos', 0.0)
        self.declare_parameter('Motor1_max_pos', 1.0)
        self.declare_parameter('Motor2_min_pos', 0.0)
        self.declare_parameter('Motor2_max_pos', 1.0)
        self.declare_parameter('left_motor_id', 8)
        self.declare_parameter('right_motor_id', 9)

        # Optional legacy self-test mode. Normal startup waits for teleop topics.
        self.declare_parameter('auto_flip', False)
        self.declare_parameter('flip_interval', 2.0)

        self.q1 = 0.0
        self.q2 = 0.0

        self.left_id = int(
            self.get_parameter('left_motor_id').get_parameter_value().integer_value
        )
        self.right_id = int(
            self.get_parameter('right_motor_id').get_parameter_value().integer_value
        )

        self.auto_flip = self.get_parameter('auto_flip').get_parameter_value().bool_value
        self.flip_interval = self.get_parameter('flip_interval').get_parameter_value().double_value
        self.is_open_ = True
        self.last_flip_time_ = time.time()

        self._init_motors()
        self._calibrate_limits()

        qos = rclpy.qos.QoSProfile(depth=10)
        self.subscriptionL = self.create_subscription(
            Float32, '/control/gripperValueL', self.left_callback, qos)
        self.subscriptionR = self.create_subscription(
            Float32, '/control/gripperValueR', self.right_callback, qos)

        self.feed_back_publisher_L = self.create_publisher(
            Float32MultiArray, 'info/gripper_feedback_L', 10)
        self.feed_back_publisher_R = self.create_publisher(
            Float32MultiArray, 'info/gripper_feedback_R', 10)
        self.feed_back_publisher_L_err = self.create_publisher(
            Int32MultiArray, 'info/gripper_feedback_L_err', 5)
        self.feed_back_publisher_R_err = self.create_publisher(
            Int32MultiArray, 'info/gripper_feedback_R_err', 5)

        self.state_publisher_L = self.create_publisher(
            Int32MultiArray, 'info/gripper_state_L', 5)
        self.state_publisher_R = self.create_publisher(
            Int32MultiArray, 'info/gripper_state_R', 5)

        self.reset_service = self.create_service(
            Trigger, 'control/reset_grippers', self.reset_motors_callback)

        # 1000 Hz 控制频率（可根据需要改为 0.01 即 100Hz）
        self.timer = self.create_timer(0.001, self.control_timer_callback)

        if self.auto_flip:
            self.get_logger().warn(
                'OmniGripper auto_flip test mode enabled; teleop commands will be overwritten.'
            )
        else:
            self.get_logger().info(
                'OmniGripper node started. Waiting for /control/gripperValueL/R commands.'
            )

    def _init_motors(self):
        global Motor1, Motor2, ZYCtrl

        Motor1 = OmniMotor(self.left_id)
        Motor2 = OmniMotor(self.right_id)

        ZYCtrl = ZYMotorControl()
        ZYCtrl.addMotor(Motor1)
        ZYCtrl.add_to_ch(Motor1, 'left')
        ZYCtrl.addMotor(Motor2)
        ZYCtrl.add_to_ch(Motor2, 'right')

        ZYCtrl.enable(Motor1)
        ZYCtrl.enable(Motor2)

    def control_timer_callback(self):
        # 自动翻转逻辑：每隔 flip_interval 秒切换一次开合度
        if self.auto_flip:
            now = time.time()
            if now - self.last_flip_time_ >= self.flip_interval:
                self.is_open_ = not self.is_open_
                self.last_flip_time_ = now
                if self.is_open_:
                    self.get_logger().info('[Auto Flip] -> Open (Pos: 1.0)')
                    self.q1 = 1.0
                    self.q2 = 1.0
                else:
                    self.get_logger().info('[Auto Flip] -> Close (Pos: 0.0)')
                    self.q1 = 0.0
                    self.q2 = 0.0

        vel_cmd = int(self.get_parameter('vel_cmd').get_parameter_value().integer_value)
        acc_cmd = int(self.get_parameter('acc_cmd').get_parameter_value().integer_value)
        dec_cmd = int(self.get_parameter('dec_cmd').get_parameter_value().integer_value)
        i_des = int(self.get_parameter('current_limit').get_parameter_value().integer_value)

        v_ratio = np.clip(vel_cmd / 100.0, 0.0, 1.0)
        a_ratio = np.clip(acc_cmd / 100.0, 0.0, 1.0)
        d_ratio = np.clip(dec_cmd / 100.0, 0.0, 1.0)
        f_ratio = np.clip(i_des / 10000.0, 0.0, 1.0)

        ZYCtrl.control_gripper(Motor1, 1.0-self.q1, v_ratio, f_ratio, a_ratio, d_ratio)
        ZYCtrl.control_gripper(Motor2, 1.0-self.q2, v_ratio, f_ratio, a_ratio, d_ratio)
        ZYCtrl.recv()

        # 左夹爪话题发布
        pos_L = Motor1.getPosition()
        vel_L = Motor1.getVelocity()
        for_L = Motor1.getTorque()
        err_L = Motor1.getErr()
        state_L = Motor1.getState()

        msgL = Float32MultiArray()
        msgL.data = [float(pos_L), float(vel_L), float(for_L), 0.0, 0.0]
        self.feed_back_publisher_L.publish(msgL)

        msgL_err = Int32MultiArray()
        msgL_err.data = [int(err_L)]
        self.feed_back_publisher_L_err.publish(msgL_err)

        msgL_state = Int32MultiArray()
        msgL_state.data = [int(state_L)]
        self.state_publisher_L.publish(msgL_state)

        # 右夹爪话题发布
        pos_R = Motor2.getPosition()
        vel_R = Motor2.getVelocity()
        for_R = Motor2.getTorque()
        err_R = Motor2.getErr()
        state_R = Motor2.getState()

        msgR = Float32MultiArray()
        msgR.data = [float(pos_R), float(vel_R), float(for_R), 0.0, 0.0]
        self.feed_back_publisher_R.publish(msgR)

        msgR_err = Int32MultiArray()
        msgR_err.data = [int(err_R)]
        self.feed_back_publisher_R_err.publish(msgR_err)

        msgR_state = Int32MultiArray()
        msgR_state.data = [int(state_R)]
        self.state_publisher_R.publish(msgR_state)

    def reset_motors_callback(self, request, response):
        ZYCtrl.disable(Motor1)
        ZYCtrl.disable(Motor2)
        time.sleep(0.1)
        ZYCtrl.enable(Motor1)
        ZYCtrl.enable(Motor2)
        response.success = True
        response.message = "OmniPicker reset successful."
        return response

    def _calibrate_limits(self):
        global Motor1_min_pos, Motor1_max_pos, Motor2_min_pos, Motor2_max_pos
        auto_calibrate = self.get_parameter('auto_calibrate').get_parameter_value().bool_value
        if auto_calibrate:
            for _ in range(50):
                ZYCtrl.control_gripper(Motor1, 0.0, 1.0, 0.5, 1.0, 1.0)
                ZYCtrl.control_gripper(Motor2, 0.0, 1.0, 0.5, 1.0, 1.0)
                ZYCtrl.recv()
                time.sleep(0.01)
            Motor1_min_pos = Motor1.getPosition()
            Motor2_min_pos = Motor2.getPosition()

            for _ in range(50):
                ZYCtrl.control_gripper(Motor1, 1.0, 1.0, 0.5, 1.0, 1.0)
                ZYCtrl.control_gripper(Motor2, 1.0, 1.0, 0.5, 1.0, 1.0)
                ZYCtrl.recv()
                time.sleep(0.01)
            Motor1_max_pos = Motor1.getPosition()
            Motor2_max_pos = Motor2.getPosition()
        else:
            Motor1_min_pos = (
                self.get_parameter('Motor1_min_pos').get_parameter_value().double_value
            )
            Motor2_min_pos = (
                self.get_parameter('Motor2_min_pos').get_parameter_value().double_value
            )
            Motor1_max_pos = (
                self.get_parameter('Motor1_max_pos').get_parameter_value().double_value
            )
            Motor2_max_pos = (
                self.get_parameter('Motor2_max_pos').get_parameter_value().double_value
            )

    def left_callback(self, msg: Float32):
        if ZYCtrl is None:
            return
        self.q1 = self._clamp(np.clip(msg.data, 0.0, 1.0), Motor1_min_pos, Motor1_max_pos)

    def right_callback(self, msg: Float32):
        if ZYCtrl is None:
            return
        self.q2 = self._clamp(np.clip(msg.data, 0.0, 1.0), Motor2_min_pos, Motor2_max_pos)

    def _clamp(self, v, vmin, vmax):
        return v * (vmax - vmin) + vmin

    def destroy_node(self):
        return super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    gripper_node = None
    try:
        gripper_node = OmniGripperNode()
        rclpy.spin(gripper_node)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"[main] Node error: {e}")
    finally:
        if gripper_node is not None:
            gripper_node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
