import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration

POSICIONES = {
    'reposo':    [0.0,  -0.5,  0.0, -1.5,  0.0,  1.0,  0.0],
    'extendido': [0.0,   0.0,  0.0, -1.0,  0.0,  1.5,  0.0],
    'izquierda': [1.2,  -0.5,  0.0, -1.5,  0.0,  1.0,  0.0],
    'derecha':   [-1.2, -0.5,  0.0, -1.5,  0.0,  1.0,  0.0],
    'arriba':    [0.0,  -1.2,  0.0, -0.5,  0.0,  1.8,  0.0],
    'bajo':      [0.0,   0.3,  0.0, -2.0,  0.0,  0.5,  0.0],
}

SECUENCIA = ['reposo', 'izquierda', 'arriba', 'derecha', 'bajo', 'extendido']

JOINT_NAMES = [
    'panda_joint1', 'panda_joint2', 'panda_joint3',
    'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7',
]


class MoverBrazo(Node):
    def __init__(self):
        super().__init__('mover_brazo')
        self.pub = self.create_publisher(
            JointTrajectory,
            '/panda_arm_controller/joint_trajectory',
            10,
        )
        self.indice = 0
        # Espera inicial de 2 s para que el controlador esté listo, luego cada 4 s
        self.timer = self.create_timer(4.0, self.mover)
        self.get_logger().info('Nodo MoverBrazo iniciado — secuencia: ' + ' → '.join(SECUENCIA))

    def mover(self):
        nombre = SECUENCIA[self.indice]
        posicion = POSICIONES[nombre]

        msg = JointTrajectory()
        msg.joint_names = JOINT_NAMES

        punto = JointTrajectoryPoint()
        punto.positions = posicion
        punto.velocities = [0.0] * 7
        punto.time_from_start = Duration(sec=3)

        msg.points = [punto]
        self.pub.publish(msg)

        self.get_logger().info(
            f'[{self.indice + 1}/{len(SECUENCIA)}] Moviendo a "{nombre}": {posicion}'
        )

        self.indice = (self.indice + 1) % len(SECUENCIA)


def main():
    rclpy.init()
    nodo = MoverBrazo()
    try:
        rclpy.spin(nodo)
    except KeyboardInterrupt:
        pass
    finally:
        nodo.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
