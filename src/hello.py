#!/usr/bin/env python
import rospy
from time import sleep
from std_msgs.msg import String
rospy.init_node('ros_emotion_detect_node')
pub = rospy.Publisher('hello11',String, queue_size = 100)
while not rospy.is_shutdown():
	pub.publish('hello111')
	rospy.sleep(1.0)
