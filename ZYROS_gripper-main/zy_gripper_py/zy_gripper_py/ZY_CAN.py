import time
import numpy as np
import socket
import struct
import select

class OmniMotor:
    def __init__(self, SlaveID):
        self.SlaveID = SlaveID
        self.state_pos = 0.0
        self.state_vel = 0.0
        self.state_force = 0.0
        self.state_code = 0
        self.err_code = 0

    def recv_data(self, pos: float, vel: float, force: float, state: int, err: int):
        self.state_pos = pos
        self.state_vel = vel
        self.state_force = force
        self.state_code = state
        self.err_code = err

    def getPosition(self):
        return self.state_pos

    def getVelocity(self):
        return self.state_vel

    def getTorque(self):
        return self.state_force

    def getState(self):
        return self.state_code

    def getErr(self):
        return self.err_code


class ZYMotorControl:
    def __init__(self, robot_ip=None):
        """
        基于 socketCAN 的智元夹爪控制类（不再直连网口）
        """
        self.motors_map = dict()
        self.left_ch = set()
        self.right_ch = set()

        # 创建 socketCAN，绑定到 vcan0（左）和 vcan1（右）
        self.sock0 = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
        self.sock0.bind(('vcan0',))
        self.sock1 = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
        self.sock1.bind(('vcan1',))
        print("[ZY_CAN] socketCAN initialized: vcan0, vcan1")

    def addMotor(self, Motor):
        self.motors_map[Motor.SlaveID] = Motor

    def add_to_ch(self, Motor, ch: str):
        if ch == "left":
            self.left_ch.add(Motor.SlaveID)
        elif ch == "right":
            self.right_ch.add(Motor.SlaveID)

    def control_gripper(self, Motor, pos_ratio: float, vel_ratio: float,
                        force_ratio: float, acc_ratio: float, dec_ratio: float):
        if Motor.SlaveID not in self.motors_map:
            return

        p_val = int(np.clip(pos_ratio, 0.0, 1.0) * 255)
        v_val = int(np.clip(vel_ratio, 0.0, 1.0) * 255)
        f_val = int(np.clip(force_ratio, 0.0, 1.0) * 255)
        a_val = int(np.clip(acc_ratio, 0.0, 1.0) * 255)
        d_val = int(np.clip(dec_ratio, 0.0, 1.0) * 255)

        data_buf = np.array([0x00, p_val, v_val, f_val, a_val, d_val, 0x00, 0x00], dtype=np.uint8)
        self.__send_data_can(Motor.SlaveID, data_buf)

    def enable(self, Motor):
        self.control_gripper(Motor, Motor.getPosition(), 1.0, 1.0, 1.0, 1.0)
        time.sleep(0.1)

    def disable(self, Motor):
        self.control_gripper(Motor, Motor.getPosition(), 0.5, 0.0, 1.0, 1.0)
        time.sleep(0.01)

    def __send_data_can(self, motor_id, data):
        if len(data) > 8:
            return

        # 选择对应通道的 socket
        if motor_id in self.left_ch:
            sock = self.sock0
        elif motor_id in self.right_ch:
            sock = self.sock1
        else:
            return

        # 构造标准 Linux can_frame (16 bytes)
        # can_id (4B) + can_dlc (1B) + __pad (3B) + data (8B)
        dlc = len(data)
        payload = data.astype(np.uint8).tobytes().ljust(8, b'\x00')
        frame = struct.pack("<IB3x8s", motor_id, dlc, payload)

        try:
            sock.send(frame)
        except Exception as e:
            print(f"[ZY_CAN] send error: {e}")

    def recv(self):
        """非阻塞轮询读取 vcan0 / vcan1 的 CAN 帧"""
        readable, _, _ = select.select([self.sock0, self.sock1], [], [], 0.001)
        for s in readable:
            try:
                frame_data = s.recv(16)
                if len(frame_data) == 16:
                    can_id = struct.unpack("<I", frame_data[0:4])[0]
                    dlc = frame_data[4]
                    packet_data = frame_data[8:8 + dlc]
                    if can_id in self.motors_map:
                        self.__process_packet(packet_data, can_id)
            except Exception as e:
                print(f"[ZY_CAN] recv error: {e}")

    def __process_packet(self, data, CANID):
        if CANID in self.motors_map:
            motor = self.motors_map[CANID]
            if len(data) >= 5:
                fault = data[0]
                state = data[1]
                pos = data[2] / 255.0
                vel = data[3] / 255.0
                force = data[4] / 255.0
                motor.recv_data(pos, vel, force, state, fault)
