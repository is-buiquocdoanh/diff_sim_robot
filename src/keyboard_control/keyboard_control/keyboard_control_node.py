#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import tkinter as tk
from tkinter import Scale, HORIZONTAL
import threading

class KeyboardControlNode(Node):
    def __init__(self):
        super().__init__('keyboard_control_node')
        self.publisher_ = self.create_publisher(Twist, 'keyboard/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.twist = Twist()
        self.speed = 0.5  # Default speed
        self.angular_speed = 1.0  # Default angular speed

        # GUI
        self.root = tk.Tk()
        self.root.title("Robot Control")
        self.root.geometry("400x400")

        # Speed slider
        self.speed_scale = Scale(self.root, from_=0.0, to=2.0, resolution=0.1, orient=HORIZONTAL, label="Linear Speed")
        self.speed_scale.set(self.speed)
        self.speed_scale.pack()

        self.angular_scale = Scale(self.root, from_=0.0, to=2.0, resolution=0.1, orient=HORIZONTAL, label="Angular Speed")
        self.angular_scale.set(self.angular_speed)
        self.angular_scale.pack()

        # Canvas for arrows
        self.canvas = tk.Canvas(self.root, width=300, height=300)
        self.canvas.pack()

        # Draw arrows
        self.draw_arrows()

        # Bind keyboard events
        self.root.bind('<KeyPress>', self.key_press)
        self.root.bind('<KeyRelease>', self.key_release)

        # Mouse events
        self.canvas.bind('<Button-1>', self.mouse_click)

        # Start GUI in separate thread
        # self.gui_thread = threading.Thread(target=self.root.mainloop)
        # self.gui_thread.start()

    def draw_arrows(self):
        # Clear canvas
        self.canvas.delete("all")
        # Up arrow
        self.canvas.create_polygon(150, 50, 130, 100, 170, 100, fill="blue", tags="up")
        # Down arrow
        self.canvas.create_polygon(150, 250, 130, 200, 170, 200, fill="blue", tags="down")
        # Left arrow
        self.canvas.create_polygon(50, 150, 100, 130, 100, 170, fill="blue", tags="left")
        # Right arrow
        self.canvas.create_polygon(250, 150, 200, 130, 200, 170, fill="blue", tags="right")

    def key_press(self, event):
        if event.keysym == 'Up':
            self.twist.linear.x = self.speed
        elif event.keysym == 'Down':
            self.twist.linear.x = -self.speed
        elif event.keysym == 'Left':
            self.twist.angular.z = self.angular_speed
        elif event.keysym == 'Right':
            self.twist.angular.z = -self.angular_speed

    def key_release(self, event):
        if event.keysym in ['Up', 'Down']:
            self.twist.linear.x = 0.0
        elif event.keysym in ['Left', 'Right']:
            self.twist.angular.z = 0.0

    def mouse_click(self, event):
        x, y = event.x, event.y
        if 130 <= x <= 170 and 50 <= y <= 100:  # Up
            self.twist.linear.x = self.speed
            self.root.after(100, lambda: setattr(self.twist.linear, 'x', 0.0))
        elif 130 <= x <= 170 and 200 <= y <= 250:  # Down
            self.twist.linear.x = -self.speed
            self.root.after(100, lambda: setattr(self.twist.linear, 'x', 0.0))
        elif 50 <= x <= 100 and 130 <= y <= 170:  # Left
            self.twist.angular.z = self.angular_speed
            self.root.after(100, lambda: setattr(self.twist.angular, 'z', 0.0))
        elif 200 <= x <= 250 and 130 <= y <= 170:  # Right
            self.twist.angular.z = -self.angular_speed
            self.root.after(100, lambda: setattr(self.twist.angular, 'z', 0.0))

    def timer_callback(self):
        self.speed = self.speed_scale.get()
        self.angular_speed = self.angular_scale.get()
        self.publisher_.publish(self.twist)

def main(args=None):
    rclpy.init(args=args)
    node = KeyboardControlNode()
    spin_thread = threading.Thread(target=rclpy.spin, args=(node,))
    spin_thread.start()
    try:
        node.root.mainloop()
    except KeyboardInterrupt:
        pass
    finally:
        node.root.quit()
        node.destroy_node()
        rclpy.shutdown()
        spin_thread.join()

if __name__ == '__main__':
    main()