FROM  ubuntu:22.04  

# Install dependencies
RUN apt update && apt install -y
RUN apt install -y sudo

# Cài ROS2 Humble
# Cài locale
RUN apt update && apt install -y locales \
    && locale-gen en_US en_US.UTF-8 \
    && update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8

# Thiết lập biến môi trường
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Ho_Chi_Minh

RUN apt update && \
    apt install -y tzdata && \
    ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata

# Setup sources
RUN apt update && \
    apt install -y software-properties-common && \
    add-apt-repository -y universe && \
    rm -rf /var/lib/apt/lists/*

RUN apt update && apt install -y curl \
    && ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F\" '{print $4}') \
    && curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb" \
    && dpkg -i /tmp/ros2-apt-source.deb \
    && rm -f /tmp/ros2-apt-source.deb

# Cài ROS2 Humble
RUN apt update && apt install -y ros-humble-desktop

# Cài thêm các gói cần thiết
RUN apt install -y \
    ros-humble-rviz2 \
    ros-humble-rplidar-ros \
    ros-humble-joint-state-publisher \
    ros-humble-joint-state-publisher-gui \
    ros-humble-robot-state-publisher \
    ros-humble-xacro \
    ros-humble-slam-toolbox \
    ros-humble-navigation2 \
    ros-humble-nav2-bringup \
    ros-humble-gazebo-ros-pkgs \
    ros-humble-gazebo-ros2-control \
    ros-humble-joy \
    ros-humble-teleop-twist-joy \
    ros-humble-teleop-twist-keyboard \
    python3-colcon-common-extensions  \
    ros-humble-cartographer \
    ros-humble-cartographer-ros


# Tạo workspace ROS2
WORKDIR /home/ros2_ws

# Copy source code vào container
COPY src ./src

# Thiết lập môi trường ROS2
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
RUN echo "source /home/ros2_ws/install/setup.bash" >> ~/.bashrc

# Build workspace
CMD ["bash"]


