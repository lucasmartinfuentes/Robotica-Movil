#!/usr/bin/env python3
"""
Nodo pose_loader (Parte 1).
Por implementar: lectura de poses desde archivo y envio a dead_reckoning_nav.
"""

import rclpy
from rclpy.node import Node


class PoseLoader(Node):

    def __init__(self):
        super().__init__('pose_loader')


def main(args=None):
    rclpy.init(args=args)
    node = PoseLoader()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
