# KM 双电机夹爪控制模块

版本：1.0  
类型：独立夹爪低级控制  
范围：仅限夹爪控制（不包括机械臂控制）

---

## 1. 概述

该模块通过 KM CAN 驱动控制双电机并联夹爪。

包含的功能：
- 电机初始化
- MIT 位置控制
- 实时反馈读取
- 实时绘图（指令 vs 反馈）
- 安全关闭处理

---

## 2. 环境要求

支持的操作系统：
- Ubuntu = 22.04


Python：
- Python 3.8/3,10

依赖：
    pip install numpy==1.23.5 matplotlib==3.6.3

---

## 3. 文件结构

km_gripper_project/
├── km_gripper.py  
├── KM_CAN.py  
├── fx_robot.py  
├── fx_kine.py  
└── README.md  

---

## 4. 配置

设置机器人控制器的 IP 地址：

    self.robot.connect('192.168.10.190')

确保：
- 网络连接正常
- 电机已接通电源
- 配置正确的电机 ID

---

## 5. 运行

Linux：
    python3 km_gripper.py

Windows：
    python km_gripper.py

---

## 6. 控制逻辑

MIT 控制：
    controlMIT(motor, Kp, Kd, position, velocity, current)

默认参数：
- Kp = 10.0
- Kd = 0.12
- 控制频率 ≈ 100 Hz
- 位置范围：0.0 – 1.0（标准化）

---

## 7. 演示模式

当前演示模式生成正弦波运动：

    self.q1 = 0.5 + math.sin(time.time()*5) * 0.5
    self.q2 = 0.5 + math.sin(time.time()*5) * 0.5

用途：
- 功能验证
- 轨迹跟踪性能观察

集成时可替换为外部输入。

---

## 8. 绘图说明

显示两个图：
- 上图：左电机（指令 vs 反馈）
- 下图：右电机（指令 vs 反馈）

正常行为：
- 反馈跟随指令变化

异常行为：
- 大误差 → 需要调节
- 振荡 → Kp 设置过高
- 响应慢 → Kp 设置过低

---

## 9. 关闭系统

按下：
    Ctrl + C

系统将：
- 停止线程
- 安全地禁用电机

切勿在未关闭系统的情况下直接断电。

---

## 10. 安全注意事项

- 测试时先不带负载
- 验证机械限制
- 保持紧急停止按钮易于触及
- 不要超过电机额定电流

---