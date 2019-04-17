import cv2
import resnet as r

import tensorflow
import numpy
from imutils.object_detection import non_max_suppression





class readAVI():
    def __init__(self): 
        self.cap = cv2.VideoCapture('./data/Marquess-Vayamos.avi')


    def main(self):

        face_cascade = cv2.CascadeClassifier('./cascades/haarcascade_frontalface_alt.xml')
        count = 0 
        fd = open("log.txt","a")
        while( self.cap.isOpened()):
          ret, frame = self.cap.read()
 
          gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
          faces= face_cascade.detectMultiScale(gray,1.1 ,3)

          bbox_list = [(x,y,w,h) for(x,y,w,h) in faces]

#          fexpr_list = r.classify_image(frame, bbox_list)
          idx = 0
          if( len (faces)>0):
              for bbox in faces:

                  pos = (bbox[0], bbox[1])
                  xx = bbox[0]
                  yy = bbox[1]
                  wd = bbox[2]
                  ht = bbox[3]
#                  fexpr = fexpr_list[idx][0]
#                  ansEmotionNO = fexpr_list[idx][0]
#                  ansPercentage = str(fexpr_list[idx][1])
#                  r.draw_label(frame, fexpr, pos, wd, ht)
                  idx = idx + 1
		  #red rectangle
                  cv2.rectangle(frame, (xx, yy), (xx + wd, yy + ht), (0, 0, 255), 2)
              #red text
              cv2.putText(frame, str(count), (10, 30), 0, 1, (0, 8,255), 2)
	      # 0:angry ,1:happy ,2:neutral ,3:sad ,4:surprise
#	      if(ansEmotion == 1):
              fd.write( "\n:" + str(count) )
          else:
              #white text
              cv2.putText(frame, str(count), (550, 30), 0, 1, (255, 255, 255), 2)

          cv2.imshow("OutImgWindow", frame)
          # cv2.imshow('frame',frame)
          # if cv2.waitKey(1) & 0xFF == ord('q'):
          #   break
          if cv2.waitKey(1) & 0xff == ord('q'):
              print("-----------count:", count)
              break

          count = count + 1
        fd.close()
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    myAVI = readAVI()
    myAVI.main()
