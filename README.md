# OmniGripper Control Examples

OmniGripper 控制例程

This project provides control examples for the **OmniGripper Gripper**, aimed at offering complete software support for OmniGripper.
本项目为基于 **OmniGripper 夹爪** 的控制例程，旨在为 OmniGripper 提供完整的软件控制支持。

The project includes the following modules:
项目主要包含以下模块：

## Project Modules

## 项目模块

### 1. USB Python Example

### 1. USB Python 例程

Controls the OmniGripper via USB interface using Python.
用于通过 USB 接口，以 Python 方式对 OmniGripper 夹爪进行控制。

**Directory Path:**
**目录位置：**
`/OmniGripper/usb/u2canfdpy`

---

### 2. USB C++ Example

### 2. USB C++ 例程

Controls the OmniGripper via USB interface using C++.
用于通过 USB 接口，以 C++ 方式对 OmniGripper 夹爪进行控制。

**Directory Path:**
**目录位置：**
`/OmniGripper/usb/u2canfd`

---

### 3. TJFX Robot Arm Passthrough Python Example

### 3. TJFX 机械臂透传 Python 例程

Controls the OmniGripper via TJFX Robot Arm passthrough using Python.
用于通过 TJFX 机械臂透传方式，以 Python 方式对 OmniGripper 夹爪进行控制。

**Directory Path:**
**目录位置：**
`/OmniGripper/Marvin_Gripper/TJ_FX_ROBOT_CONTRL_SDK-master/SDK_PYTHON`

---

### 4. TJFX Robot Arm Passthrough C++ Example

### 4. TJFX 机械臂透传 C++ 例程

Controls the OmniGripper via TJFX Robot Arm passthrough using C++.
用于通过 TJFX 机械臂透传方式，以 C++ 方式对 OmniGripper 夹爪进行控制。

**Directory Path:**
**目录位置：**
`/OmniGripper/Marvin_Gripper/TJ_FX_ROBOT_CONTRL_SDK-master/SDK_C++`

---

### 5. TJFX Robot Arm Passthrough ROS Package

### 5. TJFX 机械臂透传 ROS 包

Integrates and controls the OmniGripper via TJFX Robot Arm passthrough in a ROS environment using a remote control handle.
用于在 ROS 环境下，用遥操手柄通过 TJFX 机械臂透传方式集成和控制 OmniGripper 夹爪。

**Directory Path:**
**目录位置：**
`OmniGripper/DMROS_gripper-main/dm_gripper_py`

---

## Project Description

## 项目说明

This project provides examples for controlling the OmniGripper in different communication methods and development environments, making it easier for developers to choose the appropriate solution for secondary development and integration.
本项目覆盖了 OmniGripper 在不同通信方式和开发环境下的控制示例，方便开发者根据自身需求选择合适的方案进行二次开发与集成。

Currently, the project includes:
目前项目主要包括：

* Python/C++ control examples based on USB

* 基于 USB 的 Python/C++ 控制例程

* Python/C++ control examples based on TJFX Robot Arm passthrough

* 基于 TJFX 机械臂透传的 Python/C++ 控制例程

* TJFX Robot Arm passthrough control package for ROS

* 基于 ROS 的 TJFX 机械臂透传控制包

With these modules, developers can quickly achieve basic control of the OmniGripper, integrate it with a robotic arm, or integrate it into a ROS system for application development.
通过以上模块，开发者可以快速完成 OmniGripper 的基础控制、机械臂集成以及 ROS 系统接入。

---

## Applicable Scenarios

## 适用场景

This project is suitable for the following scenarios:
本项目适用于以下场景：

* Basic functionality debugging of OmniGripper

* OmniGripper 夹爪基础功能调试

* Direct control of the gripper via USB

* 通过 USB 直接控制夹爪

* Passthrough control of the gripper via TJFX robot arm

* 通过 TJFX 机械臂进行夹爪透传控制

* System integration and application development in ROS environment

* 在 ROS 环境中进行系统集成与应用开发
