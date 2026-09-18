#!/usr/bin/env python3
"""
Nodo dead_reckoning_nav (Parte 1).
Por implementar: navegacion por estima (dead reckoning).
"""

import rclpy
from rclpy.node import Node


class DeadReckoningNav(Node):

    def __init__(self):
        super().__init__('dead_reckoning_nav')


def main(args=None):
    rclpy.init(args=args)
    node = DeadReckoningNav()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
