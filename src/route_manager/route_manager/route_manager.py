import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import FollowWaypoints
from geometry_msgs.msg import PoseStamped
import yaml
import math
import time

class RouteManager(Node):

    def __init__(self):
        super().__init__('route_manager')

        self.declare_parameter('route_file', '')
        route_file = self.get_parameter('route_file').get_parameter_value().string_value

        self.client = ActionClient(self, FollowWaypoints, '/follow_waypoints')

        with open(route_file, 'r') as f:
            self.route = yaml.safe_load(f)['route']

        self.get_logger().info(f"Loaded {len(self.route)} waypoints")

    def create_pose(self, wp):
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.header.stamp = self.get_clock().now().to_msg()

        pose.pose.position.x = wp['x']
        pose.pose.position.y = wp['y']

        yaw = wp.get('yaw', 0.0)
        pose.pose.orientation.z = math.sin(yaw / 2.0)
        pose.pose.orientation.w = math.cos(yaw / 2.0)

        return pose

    def send_route(self):
        goal = FollowWaypoints.Goal()
        goal.poses = [self.create_pose(wp) for wp in self.route]

        self.client.wait_for_server()
        self.get_logger().info("Sending route...")

        send_goal_future = self.client.send_goal_async(goal)
        rclpy.spin_until_future_complete(self, send_goal_future)

        goal_handle = send_goal_future.result()

        if not goal_handle.accepted:
            self.get_logger().error("Route rejected!")
            return False

        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)

        self.get_logger().info("Route finished!")
        return True

    def handle_waypoint_logic(self):
        for wp in self.route:
            if 'wait' in wp:
                self.get_logger().info(f"Waiting at {wp['name']} for {wp['wait']}s")
                time.sleep(wp['wait'])

    def run(self):
        while rclpy.ok():
            success = self.send_route()

            if success:
                self.handle_waypoint_logic()
                self.get_logger().info("Looping route...")
            else:
                self.get_logger().warn("Retrying route...")

def main():
    rclpy.init()
    node = RouteManager()
    node.run()

if __name__ == '__main__':
    main()