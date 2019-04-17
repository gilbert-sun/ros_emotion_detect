#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
 
def callback(imgmsg):

    bridge = CvBridge()

    frame = bridge.imgmsg_to_cv2(imgmsg, "bgr8")

    face_cascade = cv2.CascadeClassifier('/media/nvidia/OS_Install/pyfacV3/cascades/haarcascade_frontalface_alt.xml')

    faces = face_cascade.detectMultiScale(frame,1.1,5) 
                  	     
    faceBoxes=[cv2.rectangle(frame, (xx,yy),(xx+ww,yy+hh),(255,0,0),2) for xx,yy,ww,hh in faces ]

	#print ("{}-----1----{}".format(len(faceB
    cv2.imshow("listener1", frame)

    cv2.waitKey(1)
 
def listener():
 
    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener1', anonymous=True)
    rospy.Subscriber("CVsub", Image, callback , queue_size= 1 , buff_size = 52428800)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
if __name__ == '__main__':
    listener()
