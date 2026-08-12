from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    declare_namespace = DeclareLaunchArgument(
        "namespace",
        default_value="",
        description="Namespace for the robot"
    )

    namespace = LaunchConfiguration("namespace")

    xacro_file = PathJoinSubstitution([
        FindPackageShare("robot_description"),
        "urdf",
        "robot.urdf.xacro"
    ])

    robot_description = {
        "robot_description": Command([
            "xacro ",
            xacro_file,
            " robot_namespace:=",
            namespace,
        ])
    }

    rviz_config = PathJoinSubstitution([
        FindPackageShare("robot_description"),
        "rviz",
        "robot.rviz"
    ])

    return LaunchDescription([

        declare_namespace,

        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            namespace=namespace,
            parameters=[robot_description],
            output="screen"
        ),

        Node(
            package="joint_state_publisher_gui",
            executable="joint_state_publisher_gui",
            namespace=namespace,
            output="screen"
        ),

        Node(
            package="rviz2",
            executable="rviz2",
            arguments=["-d", rviz_config],
            output="screen"
        )

    ])