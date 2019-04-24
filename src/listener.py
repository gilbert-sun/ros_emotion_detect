#!/usr/bin/env python
import cv2
import resnet as r
import numpy as np
import tensorflow as tf
from imutils.object_detection import non_max_suppression
import roslib
import rospy
import sys
from sensor_msgs.msg import Image
from std_msgs.msg import Int16, Float64, String
from cv_bridge import CvBridge



import logging
import os
from nets import resnet_v2
from preprocessing import inception_preprocessing
import time

#----------------20181129-------------------------------------------------------------------------------
# adding  report file in term of the statistic of face type at local
# crontab -e: *-2 * * * *   -bin-sh -media-nvidia-OS_Install-pyfacV3-repodayFaceTypeEmotion.sh >> test.log
# repodayFaceTypeEmotion.sh : python client_faceType_emotion.py >> client_faceType_emotion.log 2>&1
from clientFlask1 import write_json_file,face_RepoFormat
import datetime , os
from time import time
#----------------20181129-------------------------------------------------------------------------------

bbox_list = []

class EmotionClassifier():
	def __init__(self):
		slim = tf.contrib.slim
		CLASSES = ['anger', ' happy ', 'neutral', ' sad ', 'surprise']

		image_size = 160
		checkpoints_dir = '/root/catkin_ws/src/ros_emotion_detect/src/models/inception_5/'

		logging.basicConfig(filename='result.log', filemode='w', level=logging.INFO)
		self.logger = logging.getLogger('emotion classifier')

		# loading model
		with tf.Graph().as_default():
			self.image = tf.placeholder(tf.uint8, [None, None, 3])
			self.processed_image = inception_preprocessing.preprocess_image(self.image, image_size, image_size, is_training=False)
			self.processed_images = tf.placeholder(tf.float32, [None, image_size, image_size, 3])

			with slim.arg_scope(resnet_v2.resnet_arg_scope()):
				logits, _ = resnet_v2.resnet_v2_50(self.processed_images, num_classes=len(CLASSES), is_training=False)
				self.probs = tf.nn.softmax(logits)

			init_fn = slim.assign_from_checkpoint_fn(
				os.path.join(checkpoints_dir, 'model.ckpt-60000'),
				slim.get_model_variables('resnet_v2_50'))

			config = tf.ConfigProto()
			config.gpu_options.allow_growth = True
			config.allow_soft_placement = True
			self.sess = tf.Session(config=config)
			init_fn(self.sess)



emoC0 = EmotionClassifier()

class RosEmotion():

	def __init__(self):

		self.bridge = CvBridge()

		self._initNode = rospy.init_node('listener', anonymous=True)

		self._sub = rospy.Subscriber('/usb_cam/image_raw', Image, self.callback, queue_size=1, buff_size = 52428800)

		self._pub = rospy.Publisher('CVpub', Image, queue_size=1)

		self._pub1 = rospy.Publisher('result', String, queue_size=1)
 
		self.emoC1 = emoC0 #EmotionClassifier()

		#bridge = CvBridge()
		print("------Initial Entry Point of Emotion Detecting , Starting now ......")

#----------------20181129-------------------------------------------------------------------------------
# adding  report file in term of the statistic of face type at local
		self.newTime = 0
		self.oldTime = int(time()) 
		print ("......", self.oldTime)
#----------------20181129-------------------------------------------------------------------------------
 
	def callback(self, imgmsg):
		face_cascade = cv2.CascadeClassifier('/opt/ros/kinetic/share/OpenCV-3.3.1-dev/haarcascades/haarcascade_frontalface_alt.xml')#./cascades/haarcascade_frontalface_alt.xml')

		frame = self.bridge.imgmsg_to_cv2(imgmsg, "bgr8")

		faces = face_cascade.detectMultiScale(
					frame,
					scaleFactor=1.1,
					minNeighbors=5)

		bbox_list = [(x, y, w, h) for (x, y, w, h) in faces]
		#print("\n","----Return Face Coordinator ......... : ", bbox_list,"\n")

		fexpr_list = r.classify_image(self.emoC1.sess, self.emoC1.image, self.emoC1.processed_image, self.emoC1.processed_images, self.emoC1.probs, self.emoC1.logger,frame, bbox_list)


	 
		for idx,bbox in  enumerate(bbox_list):
				pos = (bbox[0],bbox[1])
				xx = bbox[0]
				yy = bbox[1]
				wd = bbox[2]
				ht = bbox[3] 
				answer = fexpr_list[idx][0]
				answer1 = str(fexpr_list[idx][1])
				answer2 = ":" + str(bbox_list[idx])

				# print('----', bbox_list[idx], "===", idx, fexpr_list[idx][0],fexpr_list[idx][1])

				## ============================================================
				rospy.logout("---------------Detecting Face Loop Starting ----------------------------")
				if (answer == 0):
						rospy.loginfo("-----------Anger :" + answer1 + answer2)
						self._pub1.publish("Anger :" + answer1 + answer2)
				elif (answer == 1):
						rospy.loginfo("---------Happy :" + answer1 + answer2)
						self._pub1.publish("Happy :" + answer1 + answer2)
				elif (answer == 2):
						rospy.loginfo("-------- Neutral :" + answer1 + answer2)
						self._pub1.publish("Neutral :" + answer1 + answer2)
				elif (answer == 3):
						rospy.loginfo("-------- Sad :" + answer1 + answer2)
						self._pub1.publish("Sad :" + answer1 + answer2)
				else:
						rospy.loginfo("----------------unkwone  emotion :" + answer1 + answer2)
						self._pub1.publish("unkwone  emotion :" + answer1 + answer2)

				r.draw_label(frame, answer, pos, wd, ht)
				#cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
				cv2.rectangle(frame, pos , (xx + wd, yy + ht), (0, 0, 255), 2)

#----------------20181129-------------------------------------------------------------------------------
# adding  report file in term of the statistic of face type at local
# crontab -e 
				self.newTime = int(time())
				if(  self.newTime - self.oldTime > 60 ):
					ans1 =  float(answer1)
					ans1 = int (ans1*100)
					write_json_file('client_faceType_emotion.json', face_RepoFormat(answer, ans1) )
					self.oldTime = int(time())
#----------------20181129-------------------------------------------------------------------------------


		msg = self.bridge.cv2_to_imgmsg(frame , "bgr8")
		self._pub.publish(msg)
		#cv2.imshow("listener", frame)
		#	cv2.waitKey(1)
		print("---------------Detecting Loop Ending .............................")


	def main(self):
		rospy.spin()
		print("------Braking Program by User .................")
 
 
 

if __name__ == '__main__':
	rosEmo1 = RosEmotion()

	#rosEmo1.__init__()
 
	rosEmo1.main()
