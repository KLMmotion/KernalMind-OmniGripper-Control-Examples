# OmniGripper Control Examples

This project provides control examples for the **OmniGripper Gripper**, aiming to offer complete software control support for OmniGripper. The project mainly includes the following modules:

## Project Modules

### 1. USB Python Example  
Used to control the OmniGripper gripper via USB in Python.

**Directory:**
`/OmniGripper/usb/u2canfdpy`

---

### 2. USB C++ Example
Used to control the OmniGripper gripper via USB in C++.

**Directory:**
`/OmniGripper/usb/u2canfd`

---

### 3. TJFX Robotic Arm Pass-Through Python Example  
Used to control the OmniGripper gripper through the FuXi robotic arm pass-through in Python.

**Directory:**
`/OmniGripper/Marvin_Gripper/TJ_FX_ROBOT_CONTRL_SDK-master/SDK_PYTHON`

---

### 4. TJFX Robotic Arm Pass-Through C++ Example  
Used to control the OmniGripper gripper through the FuXi robotic arm pass-through in C++.

**Directory:**
`/OmniGripper/Marvin_Gripper/TJ_FX_ROBOT_CONTRL_SDK-master/SDK_C++`

---

### 5. TJFX Robotic Arm Pass-Through ROS Package  
Used to control the OmniGripper gripper in a ROS environment with a remote control handle through the FuXi robotic arm pass-through.

**Directory:**
`/OmniGripper/DMROS_gripper-main/dm_gripper_py`

---

## Project Description

This project covers control examples for OmniGripper in different communication methods and development environments, providing developers with various options for secondary development and integration.  
The project mainly includes:

- USB-based Python/C++ control examples
- FuXi robotic arm pass-through-based Python/C++ control examples
- ROS-based FuXi robotic arm pass-through control package

Through these modules, developers can quickly implement basic control of OmniGripper, integrate it with robotic arms, and incorporate it into ROS systems.

---

## Applicable Scenarios

This project is suitable for the following scenarios:

- Basic functional debugging of OmniGripper
- Direct control of the gripper via USB
- Control of the gripper through FuXi robotic arm pass-through
- System integration and application development in a ROS environment