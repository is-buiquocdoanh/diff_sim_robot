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
        default_value=os.path.join(get_package_share_directory('robot_navigation'), 'maps', 'warehouse.yaml'),
        description='Full path to the YAML map file to load'
    )

    localization_params_arg = DeclareLaunchArgument(
        'localization_params_file',
        default_value=os.path.join(get_package_share_directory('robot_navigation'),'config', 'localization_slam_toolbox.yaml'),
        description='Full path to the localization parameters file'
    )

    package_dir = get_package_share_directory('robot_navigation')
    params_file = os.path.join(package_dir, 'config', 'nav2_params_mppi.yaml')
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

    # PLANNER
    planner_server = Node(
        package='nav2_planner',
        executable='planner_server',
        name='planner_server',
        output='screen',
        parameters=[params_file]
    )

    # CONTROLLER
    controller_server = Node(
        package='nav2_controller',
        executable='controller_server',
        name='controller_server',
        output='screen',
        parameters=[params_file],
    )

    # SMOOTHER SERVER (bắt buộc)
    smoother_server = Node(
        package='nav2_smoother',
        executable='smoother_server',
        name='smoother_server',
        output='screen',
        parameters=[params_file]
    )

    # BEHAVIOR TREE NAVIGATOR
    bt_navigator = Node(
        package='nav2_bt_navigator',
        executable='bt_navigator',
        name='bt_navigator',
        output='screen',
        parameters=[params_file]
    )

    # RECOVERY SERVER (bắt buộc)
    behavior_server = Node(
        package='nav2_behaviors',
        executable='behavior_server',
        name='behavior_server',
        output='screen',
        parameters=[params_file]
    )

    # VELOCITY SMOOTHER (tùy nhưng nên có)
    velocity_smoother = Node(
        package='nav2_velocity_smoother',
        executable='velocity_smoother',
        name='velocity_smoother',
        output='screen',
        parameters=[params_file],
    )

    # ROUTE SERVER
    route_server = Node(
        package='nav2_route',
        executable='route_server',
        name='route_server',
        output='screen',
        parameters=[params_file]
    )

    # LIFECYCLE MANAGER
    lifecycle_manager_nav = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_navigation',
        output='screen',
        parameters=[{
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            'autostart': True,
            'node_names': [
                'planner_server',
                'controller_server',
                'smoother_server',
                'bt_navigator',
                'behavior_server',
                'velocity_smoother',
                'route_server',
            ]
        }]
    )

    # Delay starting navigation lifecycle manager until localization components are active
    delayed_lifecycle_manager_nav = TimerAction(
        period=2.0,
        actions=[lifecycle_manager_nav]
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
        planner_server,
        controller_server,
        smoother_server,
        bt_navigator,
        behavior_server,
        velocity_smoother,
        delayed_lifecycle_manager_nav,
        route_server,
        rviz_node
    ])