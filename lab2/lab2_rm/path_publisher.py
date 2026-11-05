#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
'''
lector del txt + publisher del camino en nav_plan
'''
class PathPublisher(Node):

    def __init__(self):
        super().__init__('path_publisher')
        self.get_logger().info('path_publisher iniciado')
        self.declare_parameter('archivo', '') #ruta del txt, llega desde el launch
        archivo = self.get_parameter('archivo').value
        self.puntos = []
        with open(archivo) as f:
            for linea in f: #cada linea es x,y
                xy = linea.split(',')
                x = float(xy[0])
                y = float(xy[1])
                self.puntos.append((x,y))
        self.get_logger().info('Puntos leídos: %d' % len(self.puntos))
        self.pub = self.create_publisher(Path, 'nav_plan', 10)
        self.create_timer(1.0, self.publicar) #repite por si follow_the_carrot parte despues

    def publicar(self): #arma el Path con todos los puntos y lo envia
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
