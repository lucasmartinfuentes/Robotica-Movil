#!/usr/bin/env python3
"""
(Parte 1 - Actividad 1.2).

Registra las coordenadas (x, y) reales y de odometria mientras el
robot se mueve, guardandolas en dos archivos de texto para su analisis.

Topicos:
- Se suscribe a /real_pose (geometry_msgs/Pose)  -> posicion real
- Se suscribe a /odom (nav_msgs/Odometry)         -> posicion estimada

Salida (se crean en la carpeta desde donde se ejecute el nodo):
- real_pose_log.csv  (columnas: x,y)
- odom_log.csv       (columnas: x,y)

Uso: correr este nodo antes de empezar el recorrido, dejarlo activo
mientras el robot se mueve, y detenerlo (Ctrl+C) al terminar.
"""

import csv
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose
from nav_msgs.msg import Odometry


class PoseRecorder(Node):

    def __init__(self):
        super().__init__('pose_recorder')

        # Archivos donde se van a ir guardando las coordenadas
        self.real_pose_file = open('real_pose_log.csv', 'w')
        self.odom_file = open('odom_log.csv', 'w')

        self.create_subscription(Pose, '/real_pose', self.real_pose_cb, 10)
        self.create_subscription(Odometry, '/odom', self.odometry_cb, 10)

    def real_pose_cb(self, msg):
        self.real_pose_file.write(f'{msg.position.x},{msg.position.y}\n')

    def odometry_cb(self, msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        self.odom_file.write(f'{x},{y}\n')


def main(args=None):
    rclpy.init(args=args)
    node = PoseRecorder()
    rclpy.spin(node)


if __name__ == '__main__':
    main()