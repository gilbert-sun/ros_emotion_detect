#!/usr/bin/env python
# license removed for brevity
import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
 
def talker():
	pub = rospy.Publisher('/tutorial/image', Image, queue_size=1)
	rospy.init_node('talker', anonymous=True)
	rate = rospy.Rate(30)
	bridge = CvBridge()
	Video = cv2.VideoCapture(1)#"Marquess-Vayamos.avi")
	face_cascade = cv2.CascadeClassifier('/media/nvidia/OS_Install/pyfacV3/cascades/haarcascade_frontalface_alt.xml')
	while not rospy.is_shutdown():
         #ret, img  
		while (Video.isOpened()):
			ret, frame = Video.read()#bridge.imgmsg_to_cv2(Image,"bgr8")#Video.read()
			faces = face_cascade.detectMultiScale(frame,1.1,5) 
			if(ret == True):

				faceBoxes=[cv2.rectangle(frame, (xx,yy),(xx+ww,yy+hh),(255,0,0),2) for xx,yy,ww,hh in faces ]
				cv2.imshow("talker", frame)

				pub.publish(bridge.cv2_to_imgmsg(frame, "bgr8"))
         	
         		if cv2.waitKey(1) & 0xff == ord("q"):
					print ("==== user breaking ... ")
					break

         		
 			else:
				rate.sleep()
				break
if __name__ == '__main__':
     try:
         talker()
     except rospy.ROSInterruptException:
         pass

