from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg_share = get_package_share_directory('robot_slam_toolbox')
    params_file = os.path.join(pkg_share, 'config', 'localization.yaml')
    rviz_config = os.path.join(pkg_share, 'rviz', 'localization.rviz')

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        DeclareLaunchArgument('rviz_config_file', default_value=rviz_config),

        Node(
            package='slam_toolbox',
            executable='localization_slam_toolbox_node',
            name='slam_toolbox',
            output='screen',
            parameters=[
                params_file,
                {
                    'use_sim_time': LaunchConfiguration('use_sim_time'),
                    'map_file_name': '/home/doanh/diff_sim_robot/src/robot_slam_toolbox/maps/mapv1',
                    'map_start_pose': [0.0, 0.0, 0.0],
                    'map_start_at_dock': False,
                    'mode': 'localization'
                }
            ],
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', LaunchConfiguration('rviz_config_file')],
            parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}],
        ),
    ])
