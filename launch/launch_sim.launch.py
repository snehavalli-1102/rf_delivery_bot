import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('rf_delivery_bot')

    world_file = os.path.join(pkg_share, 'worlds', 'indoor_delivery.sdf')
    bridge_config = os.path.join(pkg_share, 'config', 'gz_bridge.yaml')
    xacro_file = os.path.join(pkg_share, 'urdf', 'robot.xacro')

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': f'-r {world_file}'}.items()
    )

    robot_description = Command(['xacro ', xacro_file])
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description, 'use_sim_time': True}]
    )

    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        arguments=['-topic', 'robot_description', '-name', 'rf_delivery_bot', '-z', '0.2']
    )

    node_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{'config_file': bridge_config}],
        output='screen'
    )

    return LaunchDescription([gazebo, node_robot_state_publisher, spawn_entity, node_bridge])