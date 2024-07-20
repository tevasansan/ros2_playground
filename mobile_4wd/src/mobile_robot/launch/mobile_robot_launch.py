import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro


def generate_launch_description():
    robot_name = "mobile_4wd"
    name_package = "mobile_robot"
    model_relative_path = "model/robot.xacro"
    world_relative_path = "model/empty_world.world"

    model_path = os.path.join(get_package_share_directory(name_package),model_relative_path)
    world_path = os.path.join(get_package_share_directory(name_package), world_relative_path)
    robot_description = xacro.process_file(model_path).toxml()

    gazebo_ros_pkg_launch = PythonLaunchDescriptionSource(os.path.join(get_package_share_directory("gazebo_ros"), "launch", "gazebo.launch.py"))
    gazebo_launch = IncludeLaunchDescription(gazebo_ros_pkg_launch, launch_arguments={
        "world": world_path}.items())
    node_spawn_model = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        output="screen",
        arguments=["-topic", "robot_description", "-entity", robot_name])

    node_robot_state_pub = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description":robot_description, "use_sim_time":True}]
    )

    launch_description_obj = LaunchDescription()

    launch_description_obj.add_action(gazebo_launch)
    launch_description_obj.add_action(node_spawn_model)
    launch_description_obj.add_action(node_robot_state_pub)
    
    return launch_description_obj