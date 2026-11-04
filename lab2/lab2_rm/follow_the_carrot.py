#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Path, Odometry
from tf_transformations import euler_from_quaternion


class FollowTheCarrot(Node):

    def __init__(self):
        super().__init__('follow_the_carrot')
        self.get_logger().info('follow_the_carrot iniciado')
        self.path = []
        self.create_subscription(Path, 'nav_plan', self.path_cb, 10)
        self.create_subscription(Odometry, '/odom', self.odom_cb, 10)

    def path_cb(self, msj): #guarda lo recido en self.path
        self.path = []
        self.get_logger().info('Recibiendo path...')
        for pose in msj.poses:
            x = pose.pose.position.x
            y = pose.pose.position.y
            self.path.append((x, y))

        self.get_logger().info('Path recibido: %d puntos' % len(self.path))



    def odom_cb(self, msj): #lee la odometría y la imprime
        if len(self.path) == 0:
            return
        x = msj.pose.pose.position.x + self.path[0][0]
        y = msj.pose.pose.position.y + self.path[0][1] #suma offset
        qx = msj.pose.pose.orientation.x
        qy = msj.pose.pose.orientation.y
        qz = msj.pose.pose.orientation.z
        qw = msj.pose.pose.orientation.w
        roll, pitch, yaw = euler_from_quaternion([qx, qy, qz, qw])
        self.get_logger().info('Odom: x=%.2f y=%.2f yaw=%.2f' % (x, y, yaw))


def main():
    rclpy.init()
    node = FollowTheCarrot()
    rclpy.spin(node)


if __name__ == '__main__':
    main()
