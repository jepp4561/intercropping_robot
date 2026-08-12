from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    declare_namespace = DeclareLaunchArgument(
        'namespace',
        default_value='robot1',
        description='Namespace of the robot to control'
    )

    namespace = LaunchConfiguration('namespace')

    teleop = ExecuteProcess(
        cmd=[
            'gnome-terminal',
            '--',
            'ros2',
            'run',
            'teleop_twist_keyboard',
            'teleop_twist_keyboard',
            '--ros-args',
            '--remap',
            [
                'cmd_vel:=/',
                namespace,
                '/diff_drive_controller/cmd_vel'
            ],
            '-p',
            'stamped:=true',
        ],
        output='screen',
    )

    return LaunchDescription([
        declare_namespace,
        teleop,
    ])