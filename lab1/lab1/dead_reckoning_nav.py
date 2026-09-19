#!/usr/bin/env python3
"""
Nodo dead_reckoning_nav (Parte 1).
Implementa navegacion por estima (dead reckoning).
"""

import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, PoseArray


class DeadReckoningNav(Node):

    def __init__(self):
        super().__init__('dead_reckoning_nav')
        self.linear_speed = 0.2   # [m/s]
        self.angular_speed = 1.0  # [rad/s]
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.goal_list_sub = self.create_subscription(
            PoseArray, 'goal_list', self.accion_mover_cb, 10
        )

    # --- Nivel 1 ---
    def aplicar_velocidad(self, speed_command_list):
        for v, w, t in speed_command_list:
            msg = Twist()
            msg.linear.x = v
            msg.angular.z = w

            inicio = self.get_clock().now()
            segundos_transcurridos = 0.0

            while segundos_transcurridos < t:
                self.cmd_vel_pub.publish(msg)
                transcurrido = self.get_clock().now() - inicio
                segundos_transcurridos = transcurrido.nanoseconds / 1e9

    # --- Nivel 2 ---
    def mover_robot_a_destino(self, goal_pose):
        x, y, theta = goal_pose

        angulo = math.atan2(y, x)
        w1 = self.angular_speed if angulo >= 0 else -self.angular_speed
        t1 = abs(angulo) / self.angular_speed

        distancia = math.sqrt(x**2 + y**2)
        t2 = distancia / self.linear_speed

        theta_restante = theta - angulo
        w3 = self.angular_speed if theta_restante >= 0 else -self.angular_speed
        t3 = abs(theta_restante) / self.angular_speed

        speed_command_list = [
            (0.0, w1, t1),
            (self.linear_speed, 0.0, t2),
            (0.0, w3, t3),
        ]

        self.aplicar_velocidad(speed_command_list)

    # --- Nivel 3 ---
    def accion_mover_cb(self, msg):
        for pose in msg.poses:
            x = pose.position.x
            y = pose.position.y
            theta = pose.orientation.z  
            self.mover_robot_a_destino((x, y, theta))


def main(args=None):
    rclpy.init(args=args)
    node = DeadReckoningNav()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()