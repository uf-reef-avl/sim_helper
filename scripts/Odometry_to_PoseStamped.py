#! usr/bin/env python
# license removed for brevity

import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped


class odometry_to_posestamped():
    def __init__(self):
        self.pose_msg = PoseStamped()
        self.pose_pub = rospy.Publisher("/pose_stamped", PoseStamped, queue_size=50)
        rospy.Subscriber("/multirotor/truth/NED", Odometry, self.Odometry_callback)

    def Odometry_callback(self, odom_msg):
        self.pose_msg.header = odom_msg.header
        self.pose_msg.pose = odom_msg.pose.pose

        self.pose_pub.publish(self.pose_msg)


if __name__ == "__main__":
    rospy.init_node('odom_to_pose_stamped')
    otp = odometry_to_posestamped()
    rospy.spin()

 
