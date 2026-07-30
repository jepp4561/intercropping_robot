import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    pkg_intercropping = get_package_share_directory(
        'intercropping_gz'
    )

    world_file = os.path.join(
        pkg_intercropping,
        'worlds',
        'intercrop_world.sdf'
    )

    models_path = os.path.join(
        pkg_intercropping,
        'models'
    )

    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory(
                    'robot_gazebo'
                ),
                'launch',
                'gazebo.launch.py'
            )
        ),
        launch_arguments={
            'world': world_file,
            'models_path': models_path,
            'spawn_z': '0.2',
        }.items()
    )

    spawn_robot = Node(
            package='ros_gz_sim',
            executable='create',
            arguments=[
                '-name', 'robot',
                '-topic', 'robot_description',
                '-z', '0.2',
            ],
            output='screen'
        )

    joint_state_broadcaster = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'joint_state_broadcaster',
            '--controller-manager',
            '/controller_manager',
        ],
        output='screen'
    )

    diff_drive_controller = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'diff_drive_controller',
            '--controller-manager',
            '/controller_manager',
        ],
        output='screen'
    )

    return LaunchDescription([

        gazebo_launch,
        spawn_robot,
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
                ],
            )
        ),


    ])