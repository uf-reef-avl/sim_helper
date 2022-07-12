#!/usr/bin/env python
# license removed for brevity

import rospy
from nav_msgs.msg import Odometry
import numpy as np

class frame_conversion():
    def __init__(self):

        self.odom_pub = rospy.Publisher("/multirotor/truth/NED", PoseStamped, queue_size=50)
        rospy.Subscriber("/iris/ground_truth/state", Odometry, self.odom_callback)
        self.rot_q = np.array(0,np.pi, np.pi, 0)

    def odom_callback(self, odom_msg):
        ned_msg = Odometry()
        ned_msg.header = odom_msg.header
        # ENU to NED Conversion
        ned_q = np.array(odom_msg.pose.pose.orientation.w,
                     odom_msg.pose.pose.orientation.x,
                     odom_msg.pose.pose.orientation.y,
                     odom_msg.pose.pose.orientation.z)

        enu_q = enu_to_ned(ned_q)
        ned_msg.orientation.w = enu_q[0]  
        ned_msg.orientation.x = enu_q[1]  
        ned_msg.orientation.y = enu_q[2]  
        ned_msg.orientation.z = enu_q[3]  

        ned_msg.pose.x = odom_msg.pose.pose.y
        ned_msg.pose.y = odom_msg.pose.pose.x
        ned_msg.pose.z = -odom_msg.pose.pose.z

        self.odom_pub.publish(ned_msg)

    def enu_to_ned(self, orientation):
        return self.rot_q @ np.transpose(orientation)
        
if __name__ == "__main__":
    frame_conversion()
