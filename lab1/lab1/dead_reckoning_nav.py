#!/usr/bin/env python3
"""
Nodo dead_reckoning_nav (Parte 1 y 3).
Implementa navegacion por estima (dead reckoning).
"""

import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, PoseArray, Vector3
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup


class DeadReckoningNav(Node):

    def __init__(self):
        super().__init__('dead_reckoning_nav')
        self.linear_speed = 0.2   # [m/s]
        self.angular_speed = 1.0  # [rad/s]
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        #self.goal_list_sub = self.create_subscription(
        #    PoseArray, 'goal_list', self.accion_mover_cb, 10)

        self.declare_parameter("factor", 1.0)
        self.factor = self.get_parameter("factor").value

        # --- Modificaciones para percepción ---
        self.grupo_movimiento = MutuallyExclusiveCallbackGroup()
        self.grupo_percepcion = MutuallyExclusiveCallbackGroup()

        self.obstacle_state = (0.0,0.0,0.0)
        self.stop = False

        self.goal_list_sub = self.create_subscription(PoseArray, 'goal_list', self.accion_mover_cb, 
                                                      10, callback_group=self.grupo_movimiento)
        self.occupancy_sub = self.create_subscription(Vector3, '/occupancy_state', self.occupancy_cb, 
                                                      10, callback_group=self.grupo_percepcion)
    # --- Nivel 1 ---
    def aplicar_velocidad(self, speed_command_list):
        for v, w, t in speed_command_list:
            msg = Twist()
            msg.linear.x = v
            msg.angular.z = w

            msg_stop = Twist()
            ultimo_tiempo = self.get_clock().now()
            segundos_transcurridos = 0.0

            while segundos_transcurridos < t:
                ahora = self.get_clock().now()
                transcurrido = (ahora - ultimo_tiempo).nanoseconds / 1e9
                ultimo_tiempo = ahora 

                x,y,z = self.obstacle_state

                # si hay un obstaculo, publicamos 0 y no sumamos los segundos transcurridos
                if x == 1.0 or y == 1.0 or z == 1.0:
                    if not self.stop:
                        self.stop = True
                        if x == 1.0:
                            self.get_logger().info("obstacle left")
                        elif y == 1.0:
                            self.get_logger().info("obstacle center")
                        elif z == 1.0:
                            self.get_logger().info("obstacle right")

                    self.cmd_vel_pub.publish(msg_stop)

                # si no hay un obstaculo se publica la velocidad normal
                else:
                    if self.stop:
                        self.stop = False

                    self.cmd_vel_pub.publish(msg)
                    segundos_transcurridos += transcurrido

    # --- Nivel 2 ---
    def mover_robot_a_destino(self, goal_pose):
        x, y, theta = goal_pose

        angulo = math.atan2(y, x)
        w1 = self.angular_speed if angulo >= 0 else -self.angular_speed
        t1 = (abs(angulo) / self.angular_speed) * self.factor

        distancia = math.sqrt(x**2 + y**2)
        t2 = distancia / self.linear_speed

        theta_restante = theta - angulo
        w3 = self.angular_speed if theta_restante >= 0 else -self.angular_speed
        t3 = (abs(theta_restante) / self.angular_speed) * self.factor

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


    # --- Funciones auxiliares Parte 3 ---
    def occupancy_cb(self,msg):
        self.obstacle_state = (msg.x,msg.y,msg.z)



def main(args=None):
    rclpy.init(args=args)
    node = DeadReckoningNav()

    exec = MultiThreadedExecutor()
    exec.add_node(node)

    try:
        exec.spin()
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()