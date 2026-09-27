#!/usr/bin/env python3
"""
Nodo obstacle_detector (Parte 3).
Procesa la imagen de profundidad y publica el estado de ocupación (Vector3).
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Vector3
import numpy as np

class ObstacleDetector(Node):

    def __init__(self):
        super().__init__('obstacle_detector')

        self.depth_sub = self.create_subscription(Image, '/camera/depth/image_raw', self.depth_cb, 10)
        self.occupancy_pub = self.create_publisher(Vector3, '/occupancy_state',10)
    
        self.umbral_distancia = 0.5 # metros

    def depth_cb(self, msg):
        depth_array = np.frombuffer(msg.data, dtype=np.float32)
        depth_image = depth_array.reshape((msg.height, msg.width))

        _,ancho = depth_image.shape
        tercio = ancho//3

        izq = depth_image[:, :tercio]
        centro = depth_image[:, tercio:2*tercio]
        der = depth_image[:, 2*tercio:]


        def hay_obstaculo(zona):

            clean_pixels = zona[np.isfinite(zona)] # limpiamos valores infinitos y NaNs
            obstacle = np.any((clean_pixels > 0.0) & (clean_pixels <= self.umbral_distancia))

            return obstacle

        msg_out = Vector3()
        msg_out.x = float(hay_obstaculo(izq))
        msg_out.y = float(hay_obstaculo(centro))
        msg_out.z = float(hay_obstaculo(der))

        self.occupancy_pub.publish(msg_out)

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()