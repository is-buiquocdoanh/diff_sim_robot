import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, TimerAction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    # Declare launch argument for use_sim_time
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation time'
    )

    package_dir = get_package_share_directory('robot_navigation')
    params_file = os.path.join(package_dir, 'config', 'nav2_params_dwb.yaml')
    rviz_config = os.path.join(package_dir, 'rviz', 'nav2_default_view.rviz')

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
        # remappings=[('/cmd_vel', '/neo_robotics/K1_demo/V0_0_0/cmd_vel')]
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
        # remappings=[('/cmd_vel', '/neo_robotics/K1_demo/V0_0_0/cmd_vel')]
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
                'velocity_smoother'
            ]
        }]
    )

    # Delay starting navigation lifecycle manager until localization components are active
    delayed_lifecycle_manager_nav = TimerAction(
        period=2.0,
        actions=[lifecycle_manager_nav]
    )

    return LaunchDescription([
        use_sim_time_arg,
        planner_server,
        controller_server,
        smoother_server,
        bt_navigator,
        behavior_server,
        velocity_smoother,
        delayed_lifecycle_manager_nav,
        # rviz_node,
        # cmd_vel_relay,
    ])