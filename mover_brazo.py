import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration

class MoverBrazo(Node):
    def __init__(self):
        super().__init__('mover_brazo')
        self.pub = self.create_publisher(
            JointTrajectory,
            '/panda_arm_controller/joint_trajectory',
            10
        )
        self.timer = self.create_timer(2.0, self.mover)

    def mover(self):
        msg = JointTrajectory()
        msg.joint_names = [
            'panda_joint1', 'panda_joint2', 'panda_joint3',
            'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7'
        ]
        punto = JointTrajectoryPoint()
        punto.positions = [0.0, -0.5, 0.0, -1.5, 0.0, 1.0, 0.0]
        punto.time_from_start = Duration(sec=2)
        msg.points = [punto]
        self.pub.publish(msg)
        self.get_logger().info('Moviendo brazo!')

def main():
    rclpy.init()
    nodo = MoverBrazo()
    rclpy.spin(nodo)

if __name__ == '__main__':
    main()