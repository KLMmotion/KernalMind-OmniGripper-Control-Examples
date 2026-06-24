# OmniGripper Control Examples

本项目为基于 **OmniGripper 夹爪** 的控制例程，旨在为 OmniGripper 提供软件控制示例支持。同时，项目新增 **智元 OmniPicker 夹爪** ROS2 控制例程，方便用户在同一工程中完成不同夹爪方案的接入和验证。项目主要包含以下模块：

## 项目模块

### 1. USB Python 例程  
用于通过 USB 接口，以 Python 方式对 OmniGripper 夹爪进行控制。

**目录位置：**
`/OmniGripper/usb/u2canfdpy`

---

### 2. USB C++ 例程
用于通过 USB 接口，以 C++ 方式对 OmniGripper 夹爪进行控制。

**目录位置：**
`/OmniGripper/usb/u2canfd`

---

### 3. TJFX 机械臂透传 Python 例程 
用于通过 TJFX 机械臂透传方式，以 Python 方式对 OmniGripper 夹爪进行控制。

**目录位置：**
`/OmniGripper/Marvin_Gripper/TJ_FX_ROBOT_CONTRL_SDK-master/SDK_PYTHON`

---

### 4. TJFX 机械臂透传 C++ 例程
用于通过 TJFX 机械臂透传方式，以 C++ 方式对 OmniGripper 夹爪进行控制。

**目录位置：**
`/OmniGripper/Marvin_Gripper/TJ_FX_ROBOT_CONTRL_SDK-master/SDK_C++`

---

### 5. TJFX 机械臂透传 ROS 包 
用于在 ROS 环境下，用遥操手柄通过 TJFX 机械臂透传方式集成和控制 OmniGripper 夹爪。

**目录位置：**
`/OmniGripper/DMROS_gripper-main/dm_gripper_py`


---

### 6. 智元 OmniPicker ROS2 例程
用于在 ROS2 环境下，通过智元 OmniPicker 夹爪的 CAN 协议完成遥操控制、状态反馈和开合测试。

**目录位置：**
`ZYROS_gripper-main/zy_gripper_py`


---

## 项目说明

本项目覆盖了 OmniGripper 在不同通信方式和开发环境下的控制示例，方便开发者根据自身需求选择合适的方案进行二次开发与集成。  
目前项目主要包括：

- 基于 USB 的 Python/C++ 控制例程
- 基于 TJFX 机械臂透传的 Python/C++ 控制例程
- 基于 ROS 的 TJFX 机械臂透传控制包
- 基于 ROS2 的智元 OmniPicker 控制例程

通过以上模块，开发者可以快速完成 OmniGripper 的基础控制、机械臂集成以及 ROS 系统接入，也可以直接参考智元 OmniPicker 的 ROS2 例程完成二次开发。

---

## 适用场景

本项目适用于以下场景：

- OmniGripper 夹爪基础功能调试
- 通过 USB 直接控制夹爪
- 通过 TJFX 机械臂进行夹爪透传控制
- 在 ROS 环境中进行系统集成与应用开发
- 在 ROS2 环境中接入和调试智元 OmniPicker 夹爪
