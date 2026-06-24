from setuptools import setup
import os
from glob import glob

package_name = 'zy_gripper_py'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # 确保 launch 文件在 colcon build 后能被安装到正确位置
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='lihaoran',
    maintainer_email='lihaoran@todo.todo',
    description='ROS 2 package for ZY OmniPicker Gripper',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # 这里将 ZY_gripper.py 里的 main 函数，注册为可执行命令 'zy_gripper_node'
            'zy_gripper_node = zy_gripper_py.ZY_gripper:main',
            'zy_gripper_auto_test = zy_gripper_py.zy_gripper_auto_test:main',
        ],
    },
)
