from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, OpaqueFunction
from launch.substitutions import LaunchConfiguration


def launch_teleop(context):
    namespace = LaunchConfiguration('namespace').perform(context)

    cmd_vel_topic = '/diff_drive_controller/cmd_vel'
    
    if namespace:
        cmd_vel_topic = f'/{namespace}{cmd_vel_topic}'

    return [
        ExecuteProcess(
            cmd=[
                'gnome-terminal',
                '--',
                'ros2',
                'run',
                'teleop_twist_keyboard',
                'teleop_twist_keyboard',
                '--ros-args',
                '--remap',
                f'cmd_vel:={cmd_vel_topic}',
                '-p',
                'stamped:=true',
            ],
            output='screen',
        )
    ]


def generate_launch_description():

    declare_namespace = DeclareLaunchArgument(
        'namespace',
        default_value='',
        description='Namespace of the robot to control'
    )

    return LaunchDescription([
        declare_namespace,
        OpaqueFunction(function=launch_teleop),
    ])