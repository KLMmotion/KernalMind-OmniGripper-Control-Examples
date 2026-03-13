#include "protocol/damiao.h"
#include <csignal>
#include <cmath>  // For sin() and M_PI
#include <iomanip>

// 原子标志，用于安全地跨线程修改
std::atomic<bool> running(true);

// Ctrl+C 触发的信号处理函数
void signalHandler(int signum) {
    running = false;
    std::cerr << "\nInterrupt signal (" << signum << ") received.\n";
}

std::shared_ptr<damiao::Motor_Control> control;

// 打印接收到的原始 CAN 帧（payload 8字节，16进制）
void print_rx_can_frame(const usb_rx_frame_t* frame) {
    constexpr size_t payload_len = 8;

    std::cerr << std::hex << std::uppercase << std::setfill('0');
    for (size_t i = 0; i < payload_len; ++i) {
        std::cerr << std::setw(2) << static_cast<int>(frame->payload[i]);
        if (i + 1 < payload_len) {
            std::cerr << " ";
        }
    }
    std::cerr << std::dec << std::endl;
}

void process_data(std::shared_ptr<damiao::Motor_Control> con, usb_rx_frame_t* frame) { 
    // 用于将接收到的数据转换为浮动值的Lambda函数
    static auto uint_to_float = [](uint16_t x, float xmin, float xmax, uint8_t bits) -> float {
        float span = xmax - xmin;  // 计算值的范围
        float data_norm = float(x) / ((1 << bits) - 1);  // 归一化数据
        float data = data_norm * span + xmin;  // 将数据映射到实际范围
        return data;
    };

    uint32_t canID = frame->head.can_id;  // 获取CAN ID（这里实际更像 mst_id）
    uint8_t ch = frame->head.channel;     // 获取通信通道

    // 打印原始16进制CAN帧
    print_rx_can_frame(frame);

    // 判断是否收到读取或写入参数的数据
    if (con->getRWSFlag() == true && con->getMotorsByChannel(ch)->find(canID) != con->getMotorsByChannel(ch)->end()) {
        if (frame->payload[2] == 0x33 || frame->payload[2] == 0x55 || frame->payload[2] == 0xAA) {
            if (frame->payload[2] == 0x33 || frame->payload[2] == 0x55) {
                con->receive_param(&frame->payload[0], ch);  // 处理读取或写入参数
                con->getRWSFlag() = false;
            }
            con->getRWSFlag() = false;
        }      
    } else {
        // 处理电机返回的正常数据（位置、速度、力矩）
        uint16_t q_uint = (uint16_t(frame->payload[1]) << 8) | frame->payload[2];
        uint16_t dq_uint = (uint16_t(frame->payload[3]) << 4) | (frame->payload[4] >> 4);
        uint16_t tau_uint = (uint16_t(frame->payload[4] & 0xf) << 8) | frame->payload[5];

        // 如果CAN ID不在电机控制列表中，返回
        if (con->getMotorsByChannel(ch)->find(canID) == con->getMotorsByChannel(ch)->end()) {
            return;
        }

        // 获取电机的参数和状态
        auto m = con->getMotorsByChannel(ch)->find(canID);
        auto limit_param_receive = m->second->get_limit_param();

        // 将接收到的原始数据转换为实际值（位置、速度、力矩）
        float receive_q = uint_to_float(q_uint, -limit_param_receive.Q_MAX, limit_param_receive.Q_MAX, 16);
        float receive_dq = uint_to_float(dq_uint, -limit_param_receive.DQ_MAX, limit_param_receive.DQ_MAX, 12);
        float receive_tau = uint_to_float(tau_uint, -limit_param_receive.TAU_MAX, limit_param_receive.TAU_MAX, 12);

        // 更新电机数据
        m->second->receive_data(receive_q, receive_dq, receive_tau); 
        m->second->updateTimeInterval();  // 更新时间间隔
    } 
}

std::mutex m_mutex;
void canframeCallback(usb_rx_frame_t* frame) { 
    std::lock_guard<std::mutex> lock(m_mutex);  // 确保线程安全
    process_data(control, frame);  
}

int main(int argc, char** argv) {
    using clock = std::chrono::steady_clock;
    using duration = std::chrono::duration<double>;

    std::signal(SIGINT, signalHandler);  // 注册信号处理函数

    try {   
        uint16_t canid1 = 0x01;  // 电机1的CAN ID
        uint16_t mstid1 = 0x11;  // 电机1的mst_id
        uint16_t canid2 = 0x02;
        uint16_t mstid2 = 0x12;
        uint32_t nom_baud = 1000000;  // 正常波特率
        uint32_t dat_baud = 5000000;  // 数据波特率

        std::vector<damiao::DmActData> init_data;  // 电机初始化数据

        // 初始化电机1
        init_data.push_back(damiao::DmActData{
            .motorType = damiao::DM4310,   // 电机类型为DM4310
            .mode = damiao::MIT_MODE,      // 控制模式为MIT模式
            .can_id = canid1,              // 设置电机CAN ID
            .mst_id = mstid1,              // 设置电机mst_id
            .channel = CHANNEL0            // 使用通信通道0
        });

        // 创建并初始化电机控制器
        control = std::make_shared<damiao::Motor_Control>(
            DEV_USB2CANFD, nom_baud, dat_baud, "4BB11E89F87B84FC6A71766BADB28A1F", &init_data);
        device_hook_to_rec(control->getUSBHw()->getDeviceHandle(), canframeCallback);  // 注册回调函数
        control->enable_all();  // 启动所有电机

        // 定义正弦轨迹控制的参数
        float amplitude = 1.0f;  // 正弦波幅度
        float frequency = 1.0f;  // 正弦波频率 (Hz)
        float kp = 1.5f;         // 刚度系数
        float kd = 0.2f;         // 阻尼系数
        float tau = 0.0f;        // 前馈力矩

        // 超速阈值，超过立即停机
        float vel_limit = 5.0f;

        const duration desired_duration(0.001);  // 控制周期：1ms（即1kHz）

        auto start_time = clock::now();
        auto current_time = clock::now();
        
        while (running) {
            current_time = clock::now();
            double elapsed_time =
                std::chrono::duration_cast<std::chrono::duration<double>>(current_time - start_time).count();
            
            // 计算目标位置：使用正弦函数控制电机的目标位置
            float pos_target = amplitude * (1.0f + std::sin(2.0 * M_PI * frequency * elapsed_time)) * 0.5f;

            // 向电机发送控制命令，控制电机位置
            // 注意：control_mit 的参数顺序是 (kp, kd, q, dq, tau)
            control->control_mit(
                *control->getMotor(CHANNEL0, canid1),  // 控制电机1
                kp,          // 刚度系数
                kd,          // 阻尼系数
                pos_target,  // 目标位置 q
                0.0f,        // 目标速度 dq
                tau          // 前馈力矩 tau
            );

            // 打印反馈信息：目标位置、实际位置、速度、力矩、时间间隔等
            float pos = control->getMotor(CHANNEL0, canid1)->Get_Position();
            float vel = control->getMotor(CHANNEL0, canid1)->Get_Velocity();
            float tau_fb = control->getMotor(CHANNEL0, canid1)->Get_tau();
            double time = control->getMotor(CHANNEL0, canid1)->getTimeInterval();
            
            std::cerr << "Motor CAN ID: " << canid1
                      << " | Target Position: " << pos_target
                      << " | Actual Position: " << pos
                      << " | Velocity: " << vel
                      << " | Torque: " << tau_fb
                      << " | Time Interval: " << time
                      << std::endl;

            // 超速保护
            if (std::fabs(vel) > vel_limit) {
                std::cerr << "[WARN] Overspeed detected! Velocity = " << vel
                          << " > " << vel_limit << ", stopping motor." << std::endl;
                break;
            }

            // 等待下一个控制周期
            std::this_thread::sleep_for(std::chrono::milliseconds(1));  // 控制周期为1ms
        }

        // 停机时失能
        control->disable_all();

        std::cout << "The program exited safely." << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "Error: hardware interface exception: " << e.what() << std::endl;
        if (control) {
            try { control->disable_all(); } catch (...) {}
        }
        return 1;
    }

    return 0;
}