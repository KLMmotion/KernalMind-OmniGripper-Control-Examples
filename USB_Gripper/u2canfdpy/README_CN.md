

# 使用USB转CANFD设备控制OmniGripper夹爪

此程序用于通过 **达妙USB转CANFD设备** 控制 OmniGripper 夹爪（DM4310 电机）。

程序默认会将电机设置为 **MIT控制模式**，使能后按照正弦轨迹发送控制指令，从而实现夹爪开合往复运动。

程序默认通信参数中，仲裁域波特率为 **1M**，数据域波特率为 **5M**。  
如果在 **5M 波特率** 下连接多个电机，请确保末端电机接入一个 **120欧电阻**，以保证通信稳定。

---

## 环境需求
python3.8/3.10
ubuntu 22.04
---

## 安装和编译

打开终端，先安装 Python 版本的 libusb 依赖，输入：

```shell
pip3 install pyusb
````

然后打开终端，输入：

```shell
mkdir -p ~/catkin_ws
cd ~/catkin_ws
```

然后把 gitee 上的 **u2canfdpy** 文件夹放到 `catkin_ws` 目录下。

如下所示：

```text
~/catkin_ws/u2canfdpy
```

---

## 简单使用

首先确认电机波特率被设置为 **5M**（夹爪出厂时已设定波特率为5M）。

然后给 **USB转CANFD设备** 设置权限，在终端输入：

```shell
sudo nano /etc/udev/rules.d/99-usb.rules
```

然后写入内容：

```shell
SUBSYSTEM=="usb", ATTR{idVendor}=="34b7", ATTR{idProduct}=="6877", MODE="0666"
```

然后重新加载并触发：

```shell
sudo udevadm control --reload-rules
sudo udevadm trigger
```

***注意：这个权限设置只需要设置 1 次，之后重新开机或插拔设备都不需要重新设置。***

然后需要通过运行 `dev_sn.py` 文件找到 **USB转CANFD设备** 的 `Serial_Number`：

```shell
cd ~/catkin_ws/u2canfdpy
python3 dev_sn.py
```

运行后，输出中 `SN` 后面的一串字符就是该设备的 `Serial_Number`。

接着复制该 `Serial_Number`，打开 `damiao.py`，替换程序中的设备序列号。

同时请确认程序中的电机参数是否与实际硬件一致，主要包括：

* 电机 CAN ID
* 电机 Master ID
* 电机型号
* 控制模式

当前示例程序默认使用的电机参数为：

```python
canid1 = 0x01
mstid1 = 0x11
motorType=DM_Motor_Type.DM4310
mode=Control_Mode.MIT_MODE
```

如果您的设备参数不同，请按实际情况修改。

另外，程序中默认使用如下控制参数实现夹爪往复运动：

```python
amplitude = 1.0
frequency = 1.0
kp = 5.0
kd = 0.2
```

其中：

* `amplitude` 表示运动幅值
* `frequency` 表示往复频率
* `kp` 和 `kd` 为 MIT 控制参数

如需调整夹爪开合幅度、速度或控制手感，可根据实际情况修改这些参数。

然后打开终端运行 `damiao.py` 文件：

```shell
cd ~/catkin_ws/u2canfdpy
python3 damiao.py
```

程序运行后，夹爪会开始做开合往复运动，终端会持续输出目标位置与电机反馈信息，例如：

```shell
0.500123
canid is: 1 pos: 0.48 vel: 0.01 effort: 0.00 target: 0.5001 time(s): 0.00102
0.503256
canid is: 1 pos: 0.49 vel: 0.02 effort: 0.00 target: 0.5033 time(s): 0.00101
```

其中输出信息包括：

* 当前目标位置
* 电机实际位置
* 电机速度
* 电机力矩
* 两次反馈之间的时间间隔

这些信息可用于观察电机运行状态以及目标值与实际值之间的偏差。

程序运行过程中，可通过按下：

```shell
Ctrl + C
```

安全退出程序。

---

## 注意事项

* 电机波特率请使用 **5M**，并与程序设置保持一致。
* 如果总线上连接多个电机，在 **5M 波特率** 下请确保末端电机接入一个 **120欧电阻**。
* 请确保 `damiao.py` 中填写的 **Serial_Number** 与实际 USB 转 CANFD 设备一致。
* 请确保程序中的 **CAN ID**、**Master ID** 与电机实际参数一致。
* 运行前请确认 USB 设备权限已正确配置，否则程序可能无法访问设备。
* 如果夹爪动作幅度过大或运行速度过快，可适当减小 `amplitude` 或 `frequency` 参数。

---

## 故障排除

### 1. 无法识别 USB 转 CANFD 设备

请检查：

* 设备是否正确连接
* udev 权限是否已正确配置
* `Serial_Number` 是否填写正确

### 2. 电机没有响应

请检查：

* 电机波特率是否设置为 **5M**
* CAN ID 和 Master ID 是否设置正确
* 电机供电是否正常
* 接线是否正确

### 3. 程序报导入错误

如果出现类似如下错误：

```shell
ModuleNotFoundError: No module named 'src'
```

请检查是否在工程根目录下运行程序，并确认 `src` 目录存在。

### 4. 电机反馈异常或运动不稳定

请检查：

* 是否正确连接终端电阻
* 是否存在多个设备 ID 冲突
* 波特率配置是否一致
* USB 通信是否稳定

