FROM tiryoh/ros2-desktop-vnc:humble
RUN apt-get update && \
    apt-get -y install ros-humble-joint-state-publisher-gui