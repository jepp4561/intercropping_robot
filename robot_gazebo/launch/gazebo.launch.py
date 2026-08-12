import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    pkg_robot_gazebo = get_package_share_directory(
        'robot_gazebo'
    )

    default_world = os.path.join(
        pkg_robot_gazebo,
        'worlds',
        'test_world.sdf'
    )

    default_models_path = os.path.join(
        pkg_robot_gazebo,
        'models'
    )

    declare_world = DeclareLaunchArgument(
        'world',
        default_value=default_world
    )

    declare_models_path = DeclareLaunchArgument(
        'models_path',
        default_value=default_models_path
    )

    world_file = LaunchConfiguration('world')
    models_path = LaunchConfiguration('models_path')

    set_gz_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=models_path
    )

    gz_sim = ExecuteProcess(
        cmd=[
            'gz',
            'sim',
            '-r',
            world_file
        ],
        output='screen'
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
        ],
        output='screen'
    )

    return LaunchDescription([
        declare_world,
        declare_models_path,

        set_gz_resource_path,

        gz_sim,
        bridge,
    ])