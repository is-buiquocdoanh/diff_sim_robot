# Differential Drive Robot Simulation in ROS 2 & Gazebo

This project provides a simulation of a **two-wheel differential drive robot** in **Gazebo**, integrated with **SLAM (SLAM Toolbox / Cartographer)** and **Navigation2 (Nav2)**, allowing you to easily experiment with navigation, mapping, and control algorithms.
![diff robot](/docs/diff_robot.png)

---

## Directory Structure

- **robot_joy**: Node to control the robot using joystick or keyboard.
- **robot_mapping**: Launch files for SLAM (cartographer.launch.py, slam_toolbox.launch.py).
- **robot_navigation**: Navigation2 configuration (navigation.launch.py).
- **robot_simulation**: URDF, world, and Gazebo launch files (display.launch.py, simulation.launch.py).

---

## System Requirements

- Ubuntu 22.04 / ROS 2 Humble
- Gazebo Fortress or Gazebo Classic (depending on your ROS 2 version)
- ROS 2 packages:
  - `ros-humble-gazebo-ros-pkgs`
  - `ros-humble-nav2-bringup`
  - `ros-humble-slam-toolbox` (or `ros-humble-cartographer-ros`)
  - `teleop-twist-keyboard` (if using keyboard teleop)

---

## Installation

```bash
# Clone repository
git clone https://github.com/is-buiquocdoanh/diff_sim_robot.git

# Build workspace
cd ~/diff_sim_robot
colcon build
source install/setup.bash
```

## Run Gazebo Simulation
``` bash
# Launch Gazebo + simulated robot
ros2 launch robot_simulation simulation.launch.py
```
The simulation.launch.py file will:

- Load the robot URDF

- Spawn the robot in the world

- Launch Gazebo

## Control the Robot
You can control the robot with either keyboard or joystick:
``` bash
# Control via joystick / teleop
ros2 launch robot_joy joystick.launch.py
```

## SLAM – Mapping
Choose between SLAM Toolbox or Cartographer:
``` bash
# SLAM Toolbox
ros2 launch robot_mapping slam_toolbox.launch.py

# Or Cartographer
ros2 launch robot_mapping cartographer.launch.py

# Save map
ros2 run nav2_map_server map_saver_cli -f ~/diff_sim_robot/src/robot_mapping/maps/my_map
```
Once SLAM is running and you move the robot, maps will be saved in `robot_navigation/maps/`.

- robot_mapping/maps/my_map.pgm – map image
- robot_mapping/maps/my_map.yaml – map metadata file

You can use another map for Nav2 by changing the map parameter in the launch command.

![robot mapping](/docs/robot_mapping.gif)

# Navigation2 – Autonomous Navigation
After generating a map `(.pgm and .yaml)`:

```bash
ros2 launch robot_navigation navigation.launch.py map:=src/robot_mapping/maps/my_map.yaml
```
RViz will display the Navigation2 interface. You can then set a Goal Pose for the robot to navigate autonomously.

![robot nav2](/docs/robot_nav2.gif)

## Author
- Name: BUI QUOC DOANH
- Email: doanh762003@gmail.com
- Project: diff robot

## License
This project is released under the [MIT License](https://opensource.org/license/mit)