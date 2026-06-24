# OmniGripper Control Examples

This project provides control examples for the **OmniGripper Gripper**, aiming to offer software control example support for OmniGripper. It also includes a ROS2 control example for the **ZY OmniPicker Gripper**, so users can validate and integrate both gripper solutions in one project. The project mainly includes the following modules:

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
Used to control the OmniGripper gripper through the TJFX robotic arm pass-through in Python.

**Directory:**
`/OmniGripper/Marvin_Gripper/TJ_FX_ROBOT_CONTRL_SDK-master/SDK_PYTHON`

---

### 4. TJFX Robotic Arm Pass-Through C++ Example  
Used to control the OmniGripper gripper through the TJFX robotic arm pass-through in C++.

**Directory:**
`/OmniGripper/Marvin_Gripper/TJ_FX_ROBOT_CONTRL_SDK-master/SDK_C++`

---

### 5. TJFX Robotic Arm Pass-Through ROS Package  
Used to control the OmniGripper gripper in a ROS environment with a remote control handle through the FuXi robotic arm pass-through.

**Directory:**
`/OmniGripper/DMROS_gripper-main/dm_gripper_py`

---

### 6. ZY OmniPicker ROS2 Example
Used to control the ZY OmniPicker gripper in a ROS2 environment through its CAN protocol, including teleoperation, feedback, and open/close testing.

**Directory:**
`ZYROS_gripper-main/zy_gripper_py`

---

## Project Description

This project covers control examples for OmniGripper in different communication methods and development environments, providing developers with various options for secondary development and integration.  
The project mainly includes:

- USB-based Python/C++ control examples
- TJFX robotic arm pass-through-based Python/C++ control examples
- ROS-based TJFX robotic arm pass-through control package
- ROS2-based ZY OmniPicker control example

Through these modules, developers can quickly implement basic control of OmniGripper, integrate it with robotic arms, incorporate it into ROS systems, and reference the ZY OmniPicker ROS2 example for secondary development.

---

## Applicable Scenarios

This project is suitable for the following scenarios:

- Basic functional debugging of OmniGripper
- Direct control of the gripper via USB
- Control of the gripper through TJFX robotic arm pass-through
- System integration and application development in a ROS environment
- ZY OmniPicker integration and debugging in a ROS2 environment
