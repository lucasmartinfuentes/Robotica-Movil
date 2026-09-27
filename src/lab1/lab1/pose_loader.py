#!/usr/bin/env python3
"""
Nodo pose_loader (Parte 1).
Lee poses desde un archivo de texto y las publica en /goal_list.

Formato del archivo (una pose por linea):
    x, y, theta
    x, y, theta
    ...
"""

import os
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseArray, Pose
from ament_index_python.packages import get_package_share_directory


class PoseLoader(Node):

    def __init__(self):
        super().__init__('pose_loader')
        self.config_path = os.path.join(
            get_package_share_directory('lab1'), 'config', 'poses.txt'
        )

        self.goal_list_pub = self.create_publisher(PoseArray, 'goal_list', 10)
        self.publicar_poses()

    def leer_poses(self):
        """Lee el archivo de configuracion y retorna una lista de (x, y, theta)."""
        poses = []
        with open(self.config_path, 'r') as f:
            for linea in f:
                linea = linea.strip()
                if not linea:
                    continue
                x, y, theta = map(float, linea.split(','))
                poses.append((x, y, theta))
        return poses

    def publicar_poses(self):
        """Arma un PoseArray a partir de leer_poses() y lo publica."""
        poses = self.leer_poses()

        msg = PoseArray()
        for x, y, theta in poses:
            pose = Pose()
            pose.position.x = x
            pose.position.y = y
            pose.orientation.z = theta
            msg.poses.append(pose)

        while self.goal_list_pub.get_subscription_count() == 0:
            rclpy.spin_once(self, timeout_sec=0.1)

        self.goal_list_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = PoseLoader()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()