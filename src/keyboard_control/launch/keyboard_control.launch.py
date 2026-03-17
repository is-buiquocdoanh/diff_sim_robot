import launch
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    twist_mux_config = os.path.join(
        get_package_share_directory('keyboard_control'),
        'config',
        'twist_mux.yaml'
    )

    return LaunchDescription([
        Node(
            package='twist_mux',
            executable='twist_mux',
            name='twist_mux',
            parameters=[twist_mux_config],
            remappings=[
                ('cmd_vel_out', 'cmd_vel')
            ]
        ),
        Node(
            package='keyboard_control',
            executable='keyboard_control_node',
            name='keyboard_control_node',
        ),
    ])