#!/usr/bin/env python
# license removed for brevity

import rospy
from nav_msgs.msg import Odometry
import numpy as np

class frame_conversion():
    def __init__(self):

        self.odom_pub = rospy.Publisher("/multirotor/truth/NED", Odometry, queue_size=50)
        #self.rot_q = np.array([0,np.pi, np.pi, 0])
        rospy.Subscriber("/iris/ground_truth/state", Odometry, self.odom_callback)

    def odom_callback(self, odom_msg):
        ned_msg = Odometry()
        ned_msg.header = odom_msg.header
        # ENU to NED Conversion
        #ned_q = np.array([odom_msg.pose.pose.orientation.w,
                    # odom_msg.pose.pose.orientation.x,
                    # odom_msg.pose.pose.orientation.y,
                    # odom_msg.pose.pose.orientation.z])

        #enu_q = self.enu_to_ned(ned_q)
        #ned_msg.pose.pose.orientation.w = enu_q[0]  
        #ned_msg.pose.pose.orientation.x = enu_q[1]  
        #ned_msg.pose.pose.orientation.y = enu_q[2]  
        #ned_msg.pose.pose.orientation.z = enu_q[3]  

        ned_msg.pose.pose.orientation.x = odom_msg.pose.pose.orientation.y
        ned_msg.pose.pose.orientation.y = odom_msg.pose.pose.orientation.x
        ned_msg.pose.pose.orientation.z = -odom_msg.pose.pose.orientation.z

        ned_msg.pose.pose.position.x = odom_msg.pose.pose.position.y
        ned_msg.pose.pose.position.y = odom_msg.pose.pose.position.x
        ned_msg.pose.pose.position.z = -odom_msg.pose.pose.position.z

        self.odom_pub.publish(ned_msg)

    def enu_to_ned(self, orientation):
        return np.multiply(self.rot_q,np.transpose(orientation))
        
if __name__ == "__main__":
    frame_conversion()
