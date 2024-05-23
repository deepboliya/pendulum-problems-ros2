#!/usr/bin/env python3
import rclpy
import numpy as np
from rclpy.node import Node
from custom_msgs.msg import States,TorqueInput
import matplotlib.pyplot as plt
import time
class pendulum_swing(Node):
    def __init__(self):
        super().__init__("pose_subscriber")
        self.subscriber = self.create_subscription(States,"/state_feedback",self.callback1,10)
        self.publisher = self.create_publisher(TorqueInput,"/torque_input",10)
        #self.timer = self.create_timer(4,self.send_torque)
        self.theta = 0 - (np.random.rand() - 0.5) / 2
        self.theta = (self.theta + np.pi)%(2*np.pi) - np.pi
        self.theta_dot = 0
        self.torque = 0
        self.setpoint  = np.pi
        
        self.t_start = time.time()
        self.t_prev = time.time() - 0.0001
        self.integral = 0
        self.previous_error = self.setpoint - self.theta


        self.Kp= 50
        self.Ki = 0
        self.Kd = 6

        self.theta_values = []
        self.time_values = []

        self.swing_up_threshold = 0.125
        self.energy_target = 8.5  # Adjust this based on your system parameters


    def callback1(self,msg:States):
        self.theta = msg.theta
        self.theta_dot = msg.theta_dot
        t = TorqueInput()
        if self.theta > 0:
            if -self.theta + np.pi > self.swing_up_threshold:
                t.torque_value = 5.0
                self.publisher.publish(t)
            else:
                if self.theta>=0:
                    error = (np.pi - self.theta)
                if self.theta<0:
                    error = -(np.pi + self.theta)

                p = self.Kp * error
                dt = time.time() - self.t_prev
                self.t_prev = time.time()
                self.integral += error* dt
                i = self.Ki * self.integral
                d = self.Kd * (error - self.previous_error)/dt
                self.previous_error = error
                t.torque_value = (p + i + d)
                if t.torque_value>5:
                    t.torque_value = 5.0
                if t.torque_value<-5:
                    t.torque_value = -5.0
                self.publisher.publish(t)
        else :
            if -(np.pi + self.theta) > self.swing_up_threshold:
                t.torque_value = -5.0
                self.publisher.publish(t)
            else:
                if self.theta>=0:
                    error = (np.pi - self.theta)
                if self.theta<0:
                    error = -(np.pi + self.theta)

                p = self.Kp * error
                dt = time.time() - self.t_prev
                self.t_prev = time.time()
                self.integral += error* dt
                i = self.Ki * self.integral
                d = self.Kd * (error - self.previous_error)/dt
                self.previous_error = error
                t.torque_value = (p + i + d)
                if t.torque_value>5:
                    t.torque_value = 5.0
                if t.torque_value<-5:
                    t.torque_value = -5.0
                self.publisher.publish(t)


def main(args=None):
    rclpy.init(args=args)
    node = pendulum_swing()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
