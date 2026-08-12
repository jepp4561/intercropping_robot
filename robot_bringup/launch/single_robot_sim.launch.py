import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

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
        }.items()
    )

    robot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory(
                    'robot_bringup'
                ),
                'launch',
                'robot.launch.py'
            )
        ),
        launch_arguments={
            # 'robot_name': 'robot1',
            # 'robot_namespace': '/robot1',
            'x': '0.0',
            'y': '0.0',
            'z': '0.2',
            'yaw': '0.0',
        }.items()
    )

    return LaunchDescription([
        gazebo_launch,
        robot,
    ])