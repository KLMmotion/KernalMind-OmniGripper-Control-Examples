
# Control OmniGripper Gripper Using a USB-to-CANFD Device

This program is used to control the OmniGripper gripper (DM4310 motor) through a **USB-to-CANFD device**.

By default, the program sets the motor to **MIT control mode**. After enabling the motor, it sends sinusoidal trajectory control commands to realize the reciprocating opening and closing motion of the gripper.

In the default communication settings, the arbitration baud rate is **1M**, and the data baud rate is **5M**.  
If multiple motors are connected under the **5M baud rate**, please make sure that a **120-ohm resistor** is connected to the motor at the end of the bus to ensure communication stability.

---

## Environment Requirements
python3.8/3.10  
ubuntu 22.04

---

## Installation and Build

Open a terminal and first install the Python version of the libusb dependency by running:

```shell
pip3 install pyusb
````

Then open a terminal and run:

```shell
mkdir -p ~/catkin_ws
cd ~/catkin_ws
```

Then place the **u2canfd** folder from Gitee into the `catkin_ws` directory.

As shown below:

```text
~/catkin_ws/u2canfd
```

---

## Quick Start

First, make sure the motor baud rate is set to **5M** (the gripper is configured to **5M** by default when shipped from the factory).

Then set the permission for the **USB-to-CANFD device** by entering the following command in the terminal:

```shell
sudo nano /etc/udev/rules.d/99-usb.rules
```

Then add the following content:

```shell
SUBSYSTEM=="usb", ATTR{idVendor}=="34b7", ATTR{idProduct}=="6877", MODE="0666"
```

Then reload and trigger the rules:

```shell
sudo udevadm control --reload-rules
sudo udevadm trigger
```

***Note: This permission setting only needs to be configured once. After that, it does not need to be set again after rebooting the computer or unplugging/replugging the device.***

Then you need to find the `Serial_Number` of the **USB-to-CANFD device** by running the `dev_sn.py` file:

```shell
cd ~/catkin_ws/u2canfd
python3 dev_sn.py
```

After running it, the string following `SN` in the output is the device `Serial_Number`.

Then copy this `Serial_Number`, open `damiao.py`, and replace the device serial number in the program.

At the same time, please make sure the motor parameters in the program match the actual hardware, mainly including:

* Motor CAN ID
* Motor Master ID
* Motor model
* Control mode

The example program currently uses the following default motor parameters:

```python
canid1 = 0x01
mstid1 = 0x11
motorType=DM_Motor_Type.DM4310
mode=Control_Mode.MIT_MODE
```

If your device parameters are different, please modify them according to the actual configuration.

In addition, the program uses the following default control parameters to achieve the reciprocating motion of the gripper:

```python
amplitude = 1.0
frequency = 1.0
kp = 5.0
kd = 0.2
```

Where:

* `amplitude` represents the motion amplitude
* `frequency` represents the reciprocating frequency
* `kp` and `kd` are MIT control parameters

If you need to adjust the gripper opening/closing amplitude, speed, or control feel, you can modify these parameters according to your actual needs.

Then open a terminal and run the `damiao.py` file:

```shell
cd ~/catkin_ws/u2canfd
python3 damiao.py
```

After the program starts running, the gripper will begin reciprocating opening and closing motions, and the terminal will continuously output the target position and motor feedback information, for example:

```shell
0.500123
canid is: 1 pos: 0.48 vel: 0.01 effort: 0.00 target: 0.5001 time(s): 0.00102
0.503256
canid is: 1 pos: 0.49 vel: 0.02 effort: 0.00 target: 0.5033 time(s): 0.00101
```

The output information includes:

* Current target position
* Actual motor position
* Motor velocity
* Motor torque
* Time interval between two feedback messages

This information can be used to observe the motor operating status and the deviation between the target value and the actual value.

During program execution, you can press:

```shell
Ctrl + C
```

to safely exit the program.

---

## Notes

* Please use a motor baud rate of **5M** and keep it consistent with the program settings.
* If multiple motors are connected on the bus, please ensure that a **120-ohm resistor** is connected to the motor at the end of the bus under the **5M baud rate**.
* Please make sure that the **Serial_Number** filled in `damiao.py` matches the actual USB-to-CANFD device.
* Please make sure that the **CAN ID** and **Master ID** in the program match the actual motor parameters.
* Before running the program, please confirm that the USB device permissions have been configured correctly; otherwise, the program may not be able to access the device.
* If the gripper motion amplitude is too large or the motion speed is too fast, you can appropriately reduce the `amplitude` or `frequency` parameter.

---

## Troubleshooting

### 1. The USB-to-CANFD device cannot be recognized

Please check:

* Whether the device is connected properly
* Whether the udev permissions have been configured correctly
* Whether the `Serial_Number` is filled in correctly

### 2. The motor does not respond

Please check:

* Whether the motor baud rate is set to **5M**
* Whether the CAN ID and Master ID are configured correctly
* Whether the motor power supply is normal
* Whether the wiring is correct

### 3. Program import error

If an error similar to the following occurs:

```shell
ModuleNotFoundError: No module named 'src'
```

Please check whether you are running the program in the project root directory, and make sure the `src` directory exists.

### 4. Abnormal motor feedback or unstable motion

Please check:

* Whether the terminal resistor is connected correctly
* Whether there are conflicts between multiple device IDs
* Whether the baud rate settings are consistent
* Whether the USB communication is stable

