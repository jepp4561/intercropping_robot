import os

from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    RegisterEventHandler,
    OpaqueFunction,
)
from launch.event_handlers import OnProcessExit, OnProcessStart
from launch.substitutions import Command, FindExecutable, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

from ament_index_python.packages import get_package_share_directory


def launch_robot(context):

    robot_name = LaunchConfiguration('robot_name').perform(context)
    robot_namespace = LaunchConfiguration('robot_namespace').perform(context)

    x = LaunchConfiguration('x').perform(context)
    y = LaunchConfiguration('y').perform(context)
    z = LaunchConfiguration('z').perform(context)
    yaw = LaunchConfiguration('yaw').perform(context)

    pkg_robot_description = get_package_share_directory(
        'robot_description'
    )

    pkg_robot_control = get_package_share_directory(
        'robot_control'
    )

    xacro_file = os.path.join(
        pkg_robot_description,
        'urdf',
        'robot.urdf.xacro'
    )

    controllers_yaml = os.path.join(
        pkg_robot_control,
        'config',
        'controllers.yaml'
    )

    robot_description = ParameterValue(
        Command([
            FindExecutable(name='xacro'),
            ' ',
            xacro_file,
            ' ',
            'controllers_config:=',
            controllers_yaml,
            ' ',
            'robot_namespace:=',
            robot_namespace,
        ]),
        value_type=str
    )

    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        namespace=robot_namespace,
        parameters=[
            {
                'robot_description': robot_description,
            }
        ],
        output='screen',
    )

    camera_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            f'{robot_namespace}/camera/image@sensor_msgs/msg/Image@gz.msgs.Image',
            f'{robot_namespace}/camera/depth_image@sensor_msgs/msg/Image@gz.msgs.Image',
            f'{robot_namespace}/camera/camera_info@sensor_msgs/msg/CameraInfo@gz.msgs.CameraInfo',
        ],
        output='screen',
    )

    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name',
            robot_name,
            '-topic',
            f'{robot_namespace}/robot_description',
            '-x', x,
            '-y', y,
            '-z', z,
            '-Y', yaw,
        ],
        output='screen',
    )

    joint_state_broadcaster = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'joint_state_broadcaster',
            '--controller-manager',
            f'{robot_namespace}/controller_manager',
        ],
        output='screen',
    )

    diff_drive_controller = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'diff_drive_controller',
            '--controller-manager',
            f'{robot_namespace}/controller_manager',
        ],
        output='screen',
    )

    return [
        rsp,
        camera_bridge,

        RegisterEventHandler(
            OnProcessStart(
                target_action=rsp,
                on_start=[
                    spawn_robot,
                ],
            )
        ),

        RegisterEventHandler(
            OnProcessExit(
                target_action=spawn_robot,
                on_exit=[
                    joint_state_broadcaster,
                ],
            )
        ),

        RegisterEventHandler(
            OnProcessExit(
                target_action=joint_state_broadcaster,
                on_exit=[
                    diff_drive_controller,
                ]
            )
        ),
    ]


def generate_launch_description():

    return LaunchDescription([

        DeclareLaunchArgument(
            'robot_name',
            default_value='',
            description='Gazebo entity name of the robot',
        ),

        DeclareLaunchArgument(
            'robot_namespace',
            default_value='',
            description='ROS namespace of the robot',
        ),

        DeclareLaunchArgument(
            'x',
            default_value='0.0',
            description='Initial X position',
        ),

        DeclareLaunchArgument(
            'y',
            default_value='0.0',
            description='Initial Y position',
        ),

        DeclareLaunchArgument(
            'z',
            default_value='0.2',
            description='Initial Z position',
        ),

        DeclareLaunchArgument(
            'yaw',
            default_value='0.0',
            description='Initial yaw',
        ),

        OpaqueFunction(function=launch_robot),
    ])