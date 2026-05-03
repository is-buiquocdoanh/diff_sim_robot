import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, TimerAction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    # Declare launch arguments
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation time'
    )

    map_yaml_arg = DeclareLaunchArgument(
        'map',
        default_value=os.path.join(get_package_share_directory('robot_navigation'), 'maps', 'elevator.yaml'),
        description='Full path to the YAML map file to load'
    )

    localization_params_arg = DeclareLaunchArgument(
        'localization_params_file',
        default_value=os.path.join(get_package_share_directory('robot_navigation'),'config', 'h3_localization_params_v1.yaml'),
        description='Full path to the localization parameters file'
    )

    package_dir = get_package_share_directory('robot_navigation')
    params_file = os.path.join(package_dir, 'config', 'h3_nav2_params_v3_mppi.yaml')
    rviz_config = os.path.join(package_dir, 'rviz', 'nav2_default_view.rviz')

    # MAP SERVER
    map_server = Node(
        package='nav2_map_server',  
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[{'yaml_filename': LaunchConfiguration('map')},
                    {'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )

    # MAP SERVER UPDATE
    map_saver = Node(
        package='nav2_map_server',
        executable='map_saver_server',
        name='map_saver',
        output='screen',
        parameters=[params_file]
    )

    # AMCL
    amcl = Node(
        package='nav2_amcl',
        executable='amcl',
        name='amcl',
        output='screen',
        parameters=[params_file]
    )

    # Localization SLAM TOOLBOX
    start_localization_slam_toolbox_node = Node(
        parameters=[
          LaunchConfiguration('localization_params_file'),
          {'use_sim_time': LaunchConfiguration('use_sim_time')}
        ],
        package='slam_toolbox',
        executable='localization_slam_toolbox_node',
        name='slam_toolbox',
        remappings=[
        ('/map', '/map')
        ],
        output='screen')

    # LIFECYCLE MANAGER
    lifecycle_manager_loc = Node(
    package='nav2_lifecycle_manager',
    executable='lifecycle_manager',
    name='lifecycle_manager_localization',
    output='screen',
    parameters=[{
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            'autostart': True,
            'node_names': [
                'map_server',
                'map_saver',
                # 'amcl'
                # 'localization_slam_toolbox_node'
            ]
        }]
    )

    # RVIZ
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config]
    )

    return LaunchDescription([
        use_sim_time_arg,
        map_yaml_arg,
        localization_params_arg,
        map_server,
        map_saver,
        # amcl,
        lifecycle_manager_loc,
        start_localization_slam_toolbox_node,
        rviz_node
    ])