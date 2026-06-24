# ZY OmniPicker Gripper ROS2 Node

This package controls a ZY OmniPicker gripper through ROS2. The upper-level ROS2 interface is kept compatible with the existing DM gripper project, while the low-level driver is replaced by the ZY 8-byte CAN protocol.

## Current Behavior

- `zy_gripper_node` starts in teleoperation mode by default.
- It does not open and close automatically on startup.
- Teleoperation commands are received from `/control/gripperValueL` and `/control/gripperValueR`.
- The open/close loop test is kept as a separate executable: `zy_gripper_auto_test`.
- The legacy `auto_flip` parameter still exists, but its default value is `false`.

## Build

```bash
colcon build --packages-select zy_gripper_py
source install/setup.bash
```

## Run Teleoperation Node

Recommended:

```bash
ros2 launch zy_gripper_py zy_gripper.launch.py
```

Default parameters:

```bash
ros2 run zy_gripper_py zy_gripper_node
```

Publish manual commands:

```bash
ros2 topic pub --once /control/gripperValueL std_msgs/msg/Float32 "{data: 1.0}"
ros2 topic pub --once /control/gripperValueR std_msgs/msg/Float32 "{data: 1.0}"
```

Command range:

- `0.0`: closed
- `1.0`: open

## Run Open/Close Test

Start the main node first:

```bash
ros2 launch zy_gripper_py zy_gripper.launch.py
```

Then run the test publisher in another terminal:

```bash
source install/setup.bash
ros2 run zy_gripper_py zy_gripper_auto_test
```

The test node publishes alternating `1.0` and `0.0` commands to `/control/gripperValueL` and `/control/gripperValueR`. It does not access CAN directly.

Adjust test parameters:

```bash
ros2 run zy_gripper_py zy_gripper_auto_test --ros-args \
  -p flip_interval:=2.0 \
  -p open_position:=1.0 \
  -p close_position:=0.0
```

## ROS2 Interface

### Input Topics

| Topic | Type | Description |
| --- | --- | --- |
| `/control/gripperValueL` | `std_msgs/msg/Float32` | Left gripper target position, from `0.0` to `1.0`. |
| `/control/gripperValueR` | `std_msgs/msg/Float32` | Right gripper target position, from `0.0` to `1.0`. |

### Feedback Topics

| Topic | Type | Data |
| --- | --- | --- |
| `info/gripper_feedback_L` | `std_msgs/msg/Float32MultiArray` | `[position, velocity, force_ratio, 0.0, 0.0]` |
| `info/gripper_feedback_R` | `std_msgs/msg/Float32MultiArray` | `[position, velocity, force_ratio, 0.0, 0.0]` |
| `info/gripper_feedback_L_err` | `std_msgs/msg/Int32MultiArray` | `[error_code]` |
| `info/gripper_feedback_R_err` | `std_msgs/msg/Int32MultiArray` | `[error_code]` |
| `info/gripper_state_L` | `std_msgs/msg/Int32MultiArray` | `[state_code]` |
| `info/gripper_state_R` | `std_msgs/msg/Int32MultiArray` | `[state_code]` |

The last two values in `info/gripper_feedback_L/R` are fixed to `0.0` for compatibility with the old DM feedback layout.

### Service

| Service | Type | Description |
| --- | --- | --- |
| `control/reset_grippers` | `std_srvs/srv/Trigger` | Disable and re-enable both grippers. |

```bash
ros2 service call /control/reset_grippers std_srvs/srv/Trigger
```

## Parameters

| Parameter | Default | Description |
| --- | --- | --- |
| `current_limit` | `10000` | Force limit. Converted internally with `/10000.0`. |
| `vel_cmd` | `100` | Velocity limit. Converted internally with `/100.0`. |
| `acc_cmd` | `100` | Acceleration ratio. Converted internally with `/100.0`. |
| `dec_cmd` | `100` | Deceleration ratio. Converted internally with `/100.0`. |
| `left_motor_id` | `8` | Left gripper CAN ID. |
| `right_motor_id` | `9` | Right gripper CAN ID. |
| `auto_calibrate` | `false` | Run min/max calibration on startup. |
| `Motor1_min_pos` | `0.0` | Left gripper mapped minimum position. |
| `Motor1_max_pos` | `1.0` | Left gripper mapped maximum position. |
| `Motor2_min_pos` | `0.0` | Right gripper mapped minimum position. |
| `Motor2_max_pos` | `1.0` | Right gripper mapped maximum position. |
| `auto_flip` | `false` | Legacy built-in open/close test. Keep disabled for teleoperation. |
| `flip_interval` | `2.0` | Interval for legacy `auto_flip` mode. |

Example:

```bash
ros2 launch zy_gripper_py zy_gripper.launch.py \
  left_motor_id:=8 \
  right_motor_id:=9 \
  vel_cmd:=80 \
  current_limit:=8000
```

## Quick Checks

```bash
ros2 node list
ros2 topic list | grep gripper
ros2 topic echo /info/gripper_feedback_L
ros2 topic echo /info/gripper_state_L
```

If the gripper opens and closes immediately after the main node starts, check whether `auto_flip:=true` was passed manually. Normal teleoperation should keep `auto_flip:=false`.
