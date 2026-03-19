
# KM Dual-Motor Gripper Control Module (C++ version)

Version: 1.0  
Type: Standalone Gripper Control  
Scope: Gripper control only (does NOT include robotic arm control)

---

## 1. Overview

This module controls a dual-motor parallel gripper (DM4310 motors) via  **TJFX robotic arm pass-through**. The program uses **MIT mode** for controlling the gripper, which performs reciprocating motion following a sinusoidal trajectory.

This module supports:
- Motor initialization
- MIT position control
- Real-time feedback reading
- Live plotting (command vs feedback)
- Safe shutdown handling

---

## 2. Environment Requirements

Supported OS:
- Ubuntu 22.04

C++ Compiler:
- GCC 13 or higher

Dependencies:
- CMake ≥ 3.10
- **Marvin SDK** (required for robot connection)

---

## 3. Configuration

### 1. Set the robot controller's IP address

In `test_damiao.cpp`, configure the IP address of the robot controller:

```cpp
// Connect to the robotic arm
OnLinkTo(192, 168, 10, 190);
````

### 2. Initialize data structures and communication

Initialize the data structure and establish communication with the robot:

```cpp
DCSS t;
bool init = OnLinkTo(192, 168, 10, 190);
```

Ensure:

* Network connection is active
* Motors are powered
* Correct motor IDs are configured

---

## 4. Running the Program

### 1. Compile

Navigate to the `u2can/build` directory and compile the C++ program:

```bash
mkdir build
cd build
cmake ..
make
```

### 2. Run

To run the control program, use the following commands:

Linux:

```bash
./test_can
```

Windows:

```bash
test_can.exe
```

After running, the gripper will start and perform the sinusoidal trajectory motion.

---

## 5. Control Logic

The program uses **MIT control mode** to control the gripper. Every time the program runs, the gripper executes reciprocating motion. The control logic is as follows:

```cpp
dm.control_mit(M1, 2.0, 0.15, q * 1.0 + 1.0, 0, 0);
```

Parameter explanation:

* `M1`: Motor to control
* `2.0`: Position stiffness (Kp)
* `0.15`: Velocity damping (Kd)
* `q`: Target position
* `0`: Velocity target
* `0`: Current target

---

## 6. Demo Mode

The current demo generates sinusoidal motion:

```cpp
self.q1 = 0.5 + math.sin(time.time() * 5) * 0.5;
self.q2 = 0.5 + math.sin(time.time() * 5) * 0.5;
```

Used for:

* Functional verification
* Performance tracking

Replace with external input when integrating.

---

## 7. Real-time Feedback and Plotting

The program provides real-time feedback, and you can view the gripper control status as follows:

```cpp
std::cout << "motor1--- POS:" << M1.Get_Position() << " VEL:" << M1.Get_Velocity() << " CUR:" << M1.Get_tau() << std::endl;
std::cout << "motor2--- POS:" << M2.Get_Position() << " VEL:" << M2.Get_Velocity() << " CUR:" << M2.Get_tau() << std::endl;
```

Additionally, the program supports real-time plotting using **matplotlib** to display the command vs feedback information (position, velocity, torque).

---

## 8. Safe Shutdown

To stop the program, press **Ctrl + C**:

```bash
Ctrl + C
```

The system will:

* Stop the threads
* Safely disable the motors

Do not power off the system directly without performing a proper shutdown.

---

## 9. Notes

* **Test without load first** before running the program.
* **Verify mechanical limits** to avoid overusing the motor.
* **Keep the emergency stop button accessible** in case of any unexpected behavior.
* Do not exceed the motor's rated current to avoid damage.

---

## 10. Troubleshooting

### 1. USB-to-CANFD device not recognized

Please check:

* Whether the device is correctly connected
* Whether the udev permissions are configured correctly
* Whether the `Serial Number` is entered correctly

### 2. Motor not responding

Please check:

* Whether the motor baud rate is set to **5M**
* Whether the CAN ID and Master ID are configured correctly
* Whether the motor is powered
* Whether the wiring is correct

### 3. Program import errors

If you encounter errors like:

```bash
ModuleNotFoundError: No module named 'src'
```

Please check if you are running the program from the correct directory and verify that the `src` directory exists.

### 4. Motor feedback issues or unstable motion

Please check:

* Whether the terminal resistors are correctly connected
* Whether there are conflicts between multiple device IDs
* Whether the baud rate configuration is consistent
* Whether the USB communication is stable


