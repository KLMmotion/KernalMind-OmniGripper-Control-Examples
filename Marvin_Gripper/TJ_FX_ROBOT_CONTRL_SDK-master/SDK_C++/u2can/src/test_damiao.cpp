#include "damiao.h"
#include "unistd.h"
#include <cmath>
#include "MarvinSDK.h"
#include <signal.h>
#include <iostream>

volatile sig_atomic_t stop_flag = 0;

const char* err_to_str(uint8_t err)
{
    switch (err)
    {
        case 0x8: return "Over Voltage";
        case 0x9: return "Under Voltage";
        case 0xA: return "Over Current";
        case 0xB: return "MOS Over Temperature";
        case 0xC: return "Coil Over Temperature";
        case 0xD: return "Communication Lost";
        case 0xE: return "Overload";
        default:  return "Ignore";
    }
}

void signal_handler(int signal)
{
  std::cout << "\nReceived interrupt signal. Stopping..." << std::endl;
  stop_flag = 1;
}

// '''#################################################################
// 该DEMO 为拖动控制案列

// 使用逻辑
//     1 初始化订阅数据的结构体
//     2 查验连接是否成功,失败程序直接退出
//     3 为了防止伺服有错，先清错
//     4 设置拖动类型
//     5 订阅查看设置是否成功
//     6 拖动,拖动结束,退出拖动
//     7 任务完成,下使能,释放内存使别的程序或者用户可以连接机器人
// '''#################################################################

damiao::Motor M1(damiao::DM4310, 0x01, 0x11, true);
damiao::Motor M2(damiao::DM4310, 0x02, 0x12, false);
// std::shared_ptr<SerialPort> serial;
damiao::Motor_Control dm;

int main(int argc, char *argv[])
{
  // Setup signal handler for Ctrl+C
  signal(SIGINT, signal_handler);

  // serial = std::make_shared<SerialPort>("/dev/ttyACM0", B921600);
     // 初始化订阅数据的结构体
    DCSS t;

    // 查验连接是否成功
    bool init = OnLinkTo(192,168,13,190);
    if (!init) {
        std::cerr << "failed:端口占用，连接失败!" << std::endl;
        return -1;
    } else {

        //防总线通信异常,先清错
        usleep(100000);
        OnClearSet();
        OnClearErr_A();
        OnClearErr_B();
        OnSetSend();
        usleep(100000);

        int motion_tag = 0;
        int frame_update = 0;

        for (int i = 0; i < 5; i++) {
            OnGetBuf(&t);
            std::cout << "connect frames :" << t.m_Out[0].m_OutFrameSerial << std::endl;

            if (t.m_Out[0].m_OutFrameSerial != 0 &&
                frame_update != t.m_Out[0].m_OutFrameSerial) {
                motion_tag++;
                frame_update = t.m_Out[0].m_OutFrameSerial;
            }
            usleep(100000);
        }

        if (motion_tag > 0) {
            std::cout << "success:机器人连接成功!" << std::endl;
        } else {
            std::cerr << "failed:机器人连接失败!" << std::endl;
            return -1;
        }
    }

    //为了防止伺服有错，先清错
    OnClearSet();
    OnClearErr_A();
    OnClearErr_B();
    OnSetSend();
    usleep(100000);

    //设置位置模式和速度保障连接：听上使能声音'
    OnClearSet();
    OnSetTargetState_A(1) ;
    OnSetTargetState_B(1) ;
    OnSetJointLmt_A(10, 10);
    OnSetJointLmt_B(10, 10);
    OnSetSend();
    sleep(1);

    //发送数据前，先清缓存
    OnClearChDataA();
    usleep(500000); 


  
  dm.addMotor(&M1);
  dm.addMotor(&M2);
  dm.disable(M1);
  usleep(100000);
  dm.disable(M2);
  sleep(1);
  bool m1_mode_ok = dm.switchControlMode(M1, damiao::MIT_MODE);
  if (m1_mode_ok)
    std::cout << "Switch to MIT_MODE Success" << std::endl;
  else
    std::cout << "Switch M1 to MIT_MODE in classical mode" << std::endl;

  usleep(100000);
  bool m2_mode_ok = dm.switchControlMode(M2, damiao::MIT_MODE);
  if (m2_mode_ok)
    std::cout << "Switch M2 to MIT_MODE Success" << std::endl;
  else
    std::cout << "Switch M2 to MIT_MODE in classical mode" << std::endl;

  // 运行时无需每次写Flash，避免写参失败导致状态异常
  // dm.save_motor_param(M1);
  // dm.save_motor_param(M2);

  // 新固件优先走标准使能；走不了则走旧固件使能方式
  if (m1_mode_ok)
    dm.enable(M1);
  else
    dm.enable_old(M1, damiao::MIT_MODE);

  usleep(100000);

  if (m2_mode_ok)
    dm.enable(M2);
  else
    dm.enable_old(M2, damiao::MIT_MODE);

  sleep(1);
  std::cout << "Press Ctrl+C to stop..." << std::endl;
  while (!stop_flag)
  {
     float q = sin(std::chrono::system_clock::now().time_since_epoch().count() / 1e9);
     dm.control_mit(M1, 2.0, 0.15, 0.75*(q * 1.0 + 1.0), 0, 0);
     dm.control_mit(M2, 2.0, 0.15, 0.75*(q * 1.0 + 1.0), 0, 0);
    // dm.control_vel(M1, q*100);
    // dm.control_pos_vel(M2, q*10,10);
    // dm.refresh_motor_status(M1);
    // dm.refresh_motor_status(M2);
    std::cout << "motor1--- POS:" << M1.Get_Position()
              << " VEL:" << M1.Get_Velocity()
              << " CUR:" << M1.Get_tau()
              << " STATE:" << int(M1.Get_Error())
              << " (" << err_to_str(M1.Get_Error()) << ")"
              << std::endl;

    std::cout << "motor2--- POS:" << M2.Get_Position()
              << " VEL:" << M2.Get_Velocity()
              << " CUR:" << M2.Get_tau()
              << " STATE:" << int(M2.Get_Error())
              << " (" << err_to_str(M2.Get_Error()) << ")"
              << std::endl;
    usleep(1000);
    //std::cout<<"motor1 pos:"<<M1.Get_Position()<<std::endl;
  }

  std::cout << "Stopping motor and cleaning up..." << std::endl;

  dm.disable(M1);
  dm.disable(M2);

  OnClearSet();
  OnSetTargetState_A(0); // 3:torque mode; 1:position mode
  OnSetSend();
  usleep(100000);
  OnRelease();

  return 0;
}
