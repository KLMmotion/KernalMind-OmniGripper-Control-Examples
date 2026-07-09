# 智元 OmniPicker 夹爪 ROS2 节点

本包用于控制智元 OmniPicker 夹爪。当前实现参考成熟的达妙夹爪工程接口，保留上层 ROS2 通信话题不变，底层替换为智元夹爪的 8 字节 CAN 协议。

## 当前状态

- 主节点 `zy_gripper_node` 默认是遥操运行状态，不会自动开合。
- 遥操入口保持为 `/control/gripperValueL` 和 `/control/gripperValueR`。
- 自动开合测试已拆成独立脚本 `zy_gripper_auto_test`，需要测试时单独运行。
- 旧版内置测试参数 `auto_flip` 仍保留，但默认关闭；正常遥操时不要开启。

## 代码结构

| 文件 | 作用 |
| --- | --- |
| `ZY_gripper.py` | ROS2 主控制节点，订阅遥操指令，周期性下发左右夹爪目标位置。 |
| `ZY_CAN.py` | 智元夹爪 CAN 通信封装，负责组包、发包、收包和状态解析。 |
| `zy_gripper_auto_test.py` | 独立开合测试发布器，只发布 ROS2 遥操话题，不直接访问 CAN。 |
| `test_gui.py` | 简单滑条发布测试工具。 |
| `launch/zy_gripper.launch.py` | 主节点启动文件，集中配置速度、力矩、CAN ID 等参数。 |

## 编译

在工作空间根目录执行：

```bash
colcon build --packages-select zy_gripper_py
source install/setup.bash
```

当前工作空间示例：

```bash
cd ZYROS_gripper-main/zy_gripper_py
colcon build --packages-select zy_gripper_py
source install/setup.bash
```

## 正常遥操启动

推荐使用 launch 启动主节点：

```bash
ros2 launch zy_gripper_py zy_gripper.launch.py
```

也可以直接运行默认参数版本：

```bash
ros2 run zy_gripper_py zy_gripper_node
```

主节点启动后会等待以下遥操话题：

```bash
/control/gripperValueL
/control/gripperValueR
```

发布值范围为 `0.0` 到 `1.0`，超出范围的输入会在节点内被限制到 `0.0` 到 `1.0`。

当前节点在下发智元夹爪 CAN 指令前会执行 `1.0 - 输入值` 的方向映射，因此本文档不固定声明 `0.0` / `1.0` 与张开、闭合的对应关系。实际方向请以夹爪安装方式和现场标定结果为准。

手动发布测试：

```bash
ros2 topic pub --once /control/gripperValueL std_msgs/msg/Float32 "{data: 1.0}"
ros2 topic pub --once /control/gripperValueR std_msgs/msg/Float32 "{data: 1.0}"
```

## 独立开合测试

先启动主节点：

```bash
ros2 launch zy_gripper_py zy_gripper.launch.py
```

再另开一个终端运行测试发布器：

```bash
source install/setup.bash
ros2 run zy_gripper_py zy_gripper_auto_test
```

测试发布器会周期性向左右夹爪发布两个端点值，用于验证通信链路和夹爪动作。它不直接控制 CAN，只通过标准遥操话题工作。

可调整测试周期和位置：

```bash
ros2 run zy_gripper_py zy_gripper_auto_test --ros-args \
  -p flip_interval:=2.0 \
  -p open_position:=1.0 \
  -p close_position:=0.0
```

如果现场测试发现开合方向与预期相反，可交换 `open_position` 和 `close_position` 的取值。

## ROS2 接口

### 输入话题

| 话题 | 类型 | 说明 |
| --- | --- | --- |
| `/control/gripperValueL` | `std_msgs/msg/Float32` | 左夹爪目标开合度，范围 `0.0` 到 `1.0`。 |
| `/control/gripperValueR` | `std_msgs/msg/Float32` | 右夹爪目标开合度，范围 `0.0` 到 `1.0`。 |

### 反馈话题

| 话题 | 类型 | 数据 |
| --- | --- | --- |
| `info/gripper_feedback_L` | `std_msgs/msg/Float32MultiArray` | `[位置, 速度, 力矩比例, 0.0, 0.0]` |
| `info/gripper_feedback_R` | `std_msgs/msg/Float32MultiArray` | `[位置, 速度, 力矩比例, 0.0, 0.0]` |
| `info/gripper_feedback_L_err` | `std_msgs/msg/Int32MultiArray` | `[故障码]` |
| `info/gripper_feedback_R_err` | `std_msgs/msg/Int32MultiArray` | `[故障码]` |
| `info/gripper_state_L` | `std_msgs/msg/Int32MultiArray` | `[状态码]` |
| `info/gripper_state_R` | `std_msgs/msg/Int32MultiArray` | `[状态码]` |

反馈数组后两位温度数据固定补 `0.0`，用于兼容达妙版本中读取 `msg.data[3]` 和 `msg.data[4]` 的旧上层代码。

### 服务

| 服务 | 类型 | 说明 |
| --- | --- | --- |
| `control/reset_grippers` | `std_srvs/srv/Trigger` | 重新 disable/enable 左右夹爪。 |

调用示例：

```bash
ros2 service call /control/reset_grippers std_srvs/srv/Trigger
```

## 状态码说明

`info/gripper_state_L` 和 `info/gripper_state_R` 的 `msg.data[0]` 表示智元夹爪内部状态：

| 状态码 | 含义 |
| --- | --- |
| `0` | 到达目标，夹爪静止。 |
| `1` | 运动中。 |
| `2` | 已夹紧或堵转，可作为抓取成功判断。 |
| `3` | 夹持过程中检测到物品掉落。 |

故障码来自智元夹爪反馈：

| 故障码 | 含义 |
| --- | --- |
| `0` | 正常。 |
| `1` | 过温。 |
| `2` | 超速。 |
| `3` | 初始化失败。 |
| `4` | 超限。 |

## 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `current_limit` | `10000` | 力矩上限。内部按 `/10000.0` 转为 `0.0` 到 `1.0`。 |
| `vel_cmd` | `100` | 速度上限。内部按 `/100.0` 转为 `0.0` 到 `1.0`。 |
| `acc_cmd` | `100` | 加速度。内部按 `/100.0` 转为 `0.0` 到 `1.0`。 |
| `dec_cmd` | `100` | 减速度。内部按 `/100.0` 转为 `0.0` 到 `1.0`。 |
| `left_motor_id` | `8` | 左夹爪 CAN ID。 |
| `right_motor_id` | `9` | 右夹爪 CAN ID。 |
| `auto_calibrate` | `false` | 启动时是否自动扫描开合极限。 |
| `Motor1_min_pos` | `0.0` | 左夹爪最小映射位置。 |
| `Motor1_max_pos` | `1.0` | 左夹爪最大映射位置。 |
| `Motor2_min_pos` | `0.0` | 右夹爪最小映射位置。 |
| `Motor2_max_pos` | `1.0` | 右夹爪最大映射位置。 |
| `auto_flip` | `false` | 旧版内置自动开合测试开关。正常遥操保持关闭。 |
| `flip_interval` | `2.0` | `auto_flip` 开启时的开合切换间隔。 |

启动时覆盖参数示例：

```bash
ros2 launch zy_gripper_py zy_gripper.launch.py \
  left_motor_id:=8 \
  right_motor_id:=9 \
  vel_cmd:=80 \
  current_limit:=8000
```

## 和达妙成熟工程的接口对齐

本包对上层保留了达妙工程里的主要通信接口：

- 输入仍然是 `/control/gripperValueL` 和 `/control/gripperValueR`。
- 反馈仍然是 `info/gripper_feedback_L/R` 和 `info/gripper_feedback_L/R_err`。
- 重置服务仍然是 `control/reset_grippers`。
- 主节点定时下发最近一次收到的目标值，默认不再自己生成开合测试动作。

底层差异：

- 达妙旧版使用 `controlMIT(...)`。
- 智元新版使用 `control_gripper(Motor, pos_ratio, vel_ratio, force_ratio, acc_ratio, dec_ratio)`。
- 智元夹爪状态机额外暴露为 `info/gripper_state_L/R`。

## 快速排查

查看主节点是否启动：

```bash
ros2 node list
```

查看遥操话题：

```bash
ros2 topic list | grep gripper
```

监听反馈：

```bash
ros2 topic echo /info/gripper_feedback_L
ros2 topic echo /info/gripper_state_L
```

确认测试脚本已安装：

```bash
ros2 run zy_gripper_py zy_gripper_auto_test
```

如果主节点一启动就自己开合，优先检查是否手动传了 `auto_flip:=true`。正常遥操模式下应保持 `auto_flip:=false`。
