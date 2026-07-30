import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    ExecuteProcess,
    SetEnvironmentVariable,
)
from launch.substitutions import (
    Command,
    FindExecutable,
    LaunchConfiguration,
)
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.actions import Node


def generate_launch_description():

    pkg_robot_description = get_package_share_directory('robot_description')
    pkg_robot_control = get_package_share_directory('robot_control')
    pkg_robot_gazebo = get_package_share_directory('robot_gazebo')


    default_world = os.path.join(
        pkg_robot_gazebo,
        'worlds',
        'test_world.sdf'
    )

    default_xacro = os.path.join(
        pkg_robot_description,
        'urdf',
        'robot.urdf.xacro'
    )

    default_controllers = os.path.join(
        pkg_robot_control,
        'config',
        'controllers.yaml'
    )

    default_models_path = os.path.join(
        pkg_robot_gazebo,
        'models'
    )


    declare_world = DeclareLaunchArgument(
        'world',
        default_value=default_world
    )

    declare_xacro = DeclareLaunchArgument(
        'xacro',
        default_value=default_xacro
    )

    declare_controllers = DeclareLaunchArgument(
        'controllers',
        default_value=default_controllers
    )

    declare_models_path = DeclareLaunchArgument(
        'models_path',
        default_value=default_models_path
    )

    declare_spawn_z = DeclareLaunchArgument(
        'spawn_z',
        default_value='0.2'
    )


    world_file = LaunchConfiguration('world')
    xacro_file = LaunchConfiguration('xacro')
    controllers_yaml = LaunchConfiguration('controllers')
    models_path = LaunchConfiguration('models_path')

    set_gz_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=models_path
    )

    robot_description = ParameterValue(
        Command([
            FindExecutable(name='xacro'),
            ' ',
            xacro_file,
            ' ',
            'controllers_config:=',
            controllers_yaml
        ]),
        value_type=str
    )

    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[
            {
                'robot_description': robot_description
            }
        ],
        output='screen'
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
            '/camera/image@sensor_msgs/msg/Image@gz.msgs.Image',
            '/camera/depth_image@sensor_msgs/msg/Image@gz.msgs.Image',
            '/camera/camera_info@sensor_msgs/msg/CameraInfo@gz.msgs.CameraInfo',
        ],
        output='screen'
    )


    return LaunchDescription([
        declare_world,
        declare_xacro,
        declare_controllers,
        declare_models_path,
        declare_spawn_z,

        set_gz_resource_path,

        gz_sim,
        rsp,
        bridge,
    ])