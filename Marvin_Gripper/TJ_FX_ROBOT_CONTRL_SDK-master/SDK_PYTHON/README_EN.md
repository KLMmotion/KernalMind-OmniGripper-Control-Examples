# KM Dual-Motor Gripper Control Module

Version: 1.0  
Type: Standalone Gripper Low-Level Control  
Scope: Gripper only (does NOT include robotic arm control)

---

## 1. Overview

This module controls a dual-motor parallel gripper using KM CAN drivers.

Functions included:
- Motor initialization
- MIT position control
- Real-time feedback reading
- Live plotting (command vs feedback)
- Safe shutdown handling

---

## 2. Environment

Supported OS:
- Ubuntu = 22.04


Python:
- Python = 3.8/3.10

Dependencies:
    pip install numpy==1.23.5 matplotlib==3.6.3

---

## 3. File Structure

SDK_PYTHON/
├── km_gripper.py
├── KM_CAN.py
├── fx_robot.py
├── fx_kine.py
└── README.md

---

## 4. Configuration

Set robot controller IP in:

    self.robot.connect('192.168.10.190')

Ensure:
- Network connected
- Motors powered
- Correct motor IDs configured

---

## 5. Run

Linux:
    python3 km_gripper.py

Windows:
    python km_gripper.py

---

## 6. Control Logic

MIT Control:
    controlMIT(motor, Kp, Kd, position, velocity, current)

Default:
- Kp = 10.0
- Kd = 0.12
- Control frequency ≈ 100 Hz
- Position range: 0.0 – 1.0 (normalized)

---

## 7. Demo Mode

Current demo generates sinusoidal motion:

    self.q1 = 0.5 + math.sin(time.time()*5) * 0.5
    self.q2 = 0.5 + math.sin(time.time()*5) * 0.5

Used for:
- Functional verification
- Tracking performance observation

Replace with external input when integrating.

---

## 8. Plot Explanation

Two plots are displayed:
- Upper: Left motor (Command vs Feedback)
- Lower: Right motor (Command vs Feedback)

Normal behavior:
- Feedback closely follows command

Abnormal:
- Large error → tuning required
- Oscillation → Kp too high
- Slow response → Kp too low

---

## 9. Shutdown

Press:
    Ctrl + C

System will:
- Stop threads
- Disable motors safely

Do NOT power off directly without shutdown.

---

## 10. Safety Notes

- Test without load first
- Verify mechanical limits
- Keep emergency stop accessible
- Do not exceed rated motor current

---
