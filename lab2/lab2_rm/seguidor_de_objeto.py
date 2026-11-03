import math
import rclpy
from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist
from lab2_rm.pid_controller import PIDController

KP = 0.5
V_LINEAL = 0.0  # cambiar a 0.2 cuando el giro funcione


class SeguidorDeObjeto(Node):
    def __init__(self):
        super().__init__('seguidor_de_objeto')
        self.setpoint_pub = self.create_publisher(Float64, 'setpoint', 1)
        self.state_pub = self.create_publisher(Float64, 'state', 1)
        self.cmd_pub = self.create_publisher(Twist, 'cmd_vel', 1)
        self.create_subscription(Float64, 'blue_square_position', self.posicion_cb, 1)
        self.create_subscription(Float64, 'control_effort', self.actuacion_cb, 1)
        self.setpoint_enviado = False

    def posicion_cb(self, msg):
        # Referencia = 0 (centro de la imagen), una vez que el controlador esté escuchando
        if not self.setpoint_enviado and self.setpoint_pub.get_subscription_count() > 0:
            self.setpoint_pub.publish(Float64(data=0.0))
            self.setpoint_enviado = True

        if math.isnan(msg.data):
            self.cmd_pub.publish(Twist())  # no se ve el cuadrado: detenerse
        else:
            self.state_pub.publish(msg)    # y(t) = posición del cuadrado

    def actuacion_cb(self, msg):
        cmd = Twist()
        cmd.linear.x = V_LINEAL
        cmd.angular.z = msg.data
        self.cmd_pub.publish(cmd)


def main():
    rclpy.init()
    executor = SingleThreadedExecutor()
    executor.add_node(PIDController(KP))
    executor.add_node(SeguidorDeObjeto())
    executor.spin()