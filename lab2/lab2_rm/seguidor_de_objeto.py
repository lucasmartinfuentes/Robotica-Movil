import math
import rclpy
from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor
from std_msgs.msg import Float64, Bool
from geometry_msgs.msg import Twist
from lab2_rm.pid_controller import PIDController

KP = 0.5
V_LINEAL = 0.1


class SeguidorDeObjeto(Node):
    def __init__(self):
        super().__init__('seguidor_de_objeto')
        self.setpoint_pub = self.create_publisher(Float64, 'setpoint', 1)
        self.state_pub = self.create_publisher(Float64, 'state', 1)
        self.cmd_pub = self.create_publisher(Twist, 'cmd_vel', 1)
        self.create_subscription(Float64, 'blue_square_position', self.posicion_cb, 1)
        self.create_subscription(Bool, 'blue_square_cerca', self.cerca_cb, 1)
        self.create_subscription(Float64, 'control_effort', self.actuacion_cb, 1)
        self.setpoint_enviado = False
        self.cerca = False

    def cerca_cb(self, msg):
        self.cerca = msg.data

    def posicion_cb(self, msg):
        if not self.setpoint_enviado and self.setpoint_pub.get_subscription_count() > 0:
            self.setpoint_pub.publish(Float64(data=0.0))
            self.setpoint_enviado = True

        if math.isnan(msg.data):
            self.cmd_pub.publish(Twist())  
        else:
            self.state_pub.publish(msg)    

    def actuacion_cb(self, msg):
        cmd = Twist()
        cmd.linear.x = 0.0 if self.cerca else V_LINEAL 
        cmd.angular.z = msg.data
        self.cmd_pub.publish(cmd)


def main():
    rclpy.init()
    executor = SingleThreadedExecutor()
    executor.add_node(PIDController(KP))
    executor.add_node(SeguidorDeObjeto())
    executor.spin()
