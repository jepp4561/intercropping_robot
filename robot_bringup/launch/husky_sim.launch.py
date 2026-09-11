import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import AppendEnvironmentVariable
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():

    pkg_intercropping = get_package_share_directory(
        "intercropping_gz"
    )

    pkg_robot_gazebo = get_package_share_directory(
        "robot_gazebo"
    )

    pkg_robot_bringup = get_package_share_directory(
        "robot_bringup"
    )

    pkg_clearpath_gz = get_package_share_directory(
        "clearpath_gz"
    )

    world_file = os.path.join(
        pkg_intercropping,
        "worlds",
        "intercrop_world.sdf",
    )

    models_path = os.path.join(
        pkg_intercropping,
        "models",
    )

    clearpath_setup_path = os.path.join(
        pkg_robot_bringup,
        "config",
        "clearpath",
        "husky",
    )

    clearpath_description_path = (
        get_package_share_directory(
            "clearpath_platform_description"
        )
    )

    soil_sampler_resource_path = os.path.dirname(
        get_package_share_directory(
            "soil_sampler_description"
        )
    )

    append_clearpath_resource_path = (
        AppendEnvironmentVariable(
            name="GZ_SIM_RESOURCE_PATH",
            value=clearpath_description_path,
        )
    )

    append_soil_sampler_resource_path = (
        AppendEnvironmentVariable(
            name="GZ_SIM_RESOURCE_PATH",
            value=soil_sampler_resource_path,
        )
    )

    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                pkg_robot_gazebo,
                "launch",
                "gazebo.launch.py",
            )
        ),
        launch_arguments={
            "world": world_file,
            "models_path": models_path,
        }.items(),
    )

    husky_spawn = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                pkg_clearpath_gz,
                "launch",
                "robot_spawn.launch.py",
            )
        ),
        launch_arguments={
            "setup_path": clearpath_setup_path,
            "generate": "true",
            "use_sim_time": "true",
            "x": "0.0",
            "y": "0.0",
            "z": "0.2",
            "yaw": "3.14159",
            "rviz": "false",
        }.items(),
    )

    soil_sampler_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory(
                    "soil_sampler_bringup"
                ),
                "launch",
                "soil_sampler_sim.launch.py",
            )
        ),
        launch_arguments={
            "robot_namespace": "husky",
            "controller_manager": (
                "/husky/controller_manager"
            ),
            "tool_namespace": "soil_sampler",
        }.items(),
    )

    return LaunchDescription([
        append_clearpath_resource_path,
        append_soil_sampler_resource_path,
        gazebo_launch,
        husky_spawn,
        soil_sampler_sim,
    ])