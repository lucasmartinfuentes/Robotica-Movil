#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
'''
lector del txt + publisher de 


'''
class PathPublisher(Node):

    def __init__(self):
        super().__init__('path_publisher')
        self.get_logger().info('path_publisher iniciado')
        self.declare_parameter('archivo', '')
        archivo = self.get_parameter('archivo').value
        self.puntos = []
        with open(archivo) as f:
            for linea in f:
                xy = linea.split(',')
                x = float(xy[0])
                y = float(xy[1])
                self.puntos.append((x,y))
        self.get_logger().info('Puntos leídos: %d' % len(self.puntos))
        self.pub = self.create_publisher(Path, 'nav_plan', 10)
        self.create_timer(1.0, self.publicar)

    def publicar(self):
        msj = Path()
        for x, y in self.puntos:
            posestamped = PoseStamped()
            posestamped.pose.position.x = x
            posestamped.pose.position.y = y
            msj.poses.append(posestamped)
        self.pub.publish(msj)
        


def main():
    rclpy.init()
    node = PathPublisher()
    rclpy.spin(node)


if __name__ == '__main__':
    main()
