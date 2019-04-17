import cv2
import resnet as r
import tensorflow as tf
import logging
import os
from nets import resnet_v2
from preprocessing import inception_preprocessing
import time




slim = tf.contrib.slim
CLASSES = ['anger', ' happy ', 'neutral', ' sad ', 'surprise']


if __name__ == "__main__":


    frames = []
    bbox_lists = []
    timeout = 1
    image_size = 160
    checkpoints_dir = 'models/inception_5/'

    logging.basicConfig(filename='result.log', filemode='w',level=logging.INFO)
    logger = logging.getLogger('emotion classifier')

    # loading model
    with tf.Graph().as_default():
        image = tf.placeholder(tf.uint8, [None, None, 3])
        processed_image = inception_preprocessing.preprocess_image(image, image_size, image_size, is_training=False)
        processed_images = tf.placeholder(tf.float32, [None, image_size, image_size, 3])

        with slim.arg_scope(resnet_v2.resnet_arg_scope()):
            logits, _ = resnet_v2.resnet_v2_50(processed_images, num_classes=len(CLASSES), is_training=False)
            probs = tf.nn.softmax(logits)

        init_fn = slim.assign_from_checkpoint_fn(
            os.path.join(checkpoints_dir, 'model.ckpt-60000'),
            slim.get_model_variables('resnet_v2_50'))

        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        config.allow_soft_placement = True
        sess = tf.Session(config=config)
        init_fn(sess)

#---------------------------------

    cap = cv2.VideoCapture(1)#breakupTeacherStudent.mp4')#Marquess-Vayamos.avi')#news_kp_partial.mp4#"./data/Marquess-Vayamos.avi"

    face_cascade = cv2.CascadeClassifier('./cascades/haarcascade_frontalface_alt.xml')
    count = 0 
    fd = open("log2.txt","a")
    Begin_localtime = time.asctime( time.localtime(time.time()) )
    print ("---Begin time :", Begin_localtime)
    fd.write("\n"+"Begin time :"+Begin_localtime)
    while( cap.isOpened()):
#    if(count <1):
        #count= count + 1
        ret, frame = cap.read()
        #frame = cv2.imread('data/789.jpg')
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        # you should adjust detectMultiScale parameter to detect faces
        faces= face_cascade.detectMultiScale(gray,1.05 ,5)
        if(len(faces)> 0):
            bbox_list = [(x,y,w,h) for(x,y,w,h) in faces]
    #---------------------------------
    #    for f_idx in range(len(frames)):
            fexpr_list = r.classify_image(sess, image, processed_image, processed_images, probs, logger,frame, bbox_list) #frames[f_idx], bbox_lists[f_idx])
            #for b_idx in range(len(bbox_lists[f_idx])):
            for b_idx in range( len(bbox_list) ): #b_idx #range( len(bbox_list) ): #faces
                bbox = bbox_list[b_idx]

                pos = (bbox[0], bbox[1])
                wd = bbox[2]
                ht = bbox[3]
               #fexpr = fexpr_list[b_idx][0]
                fexpr = fexpr_list[b_idx][0]
               #r.draw_label(frames[f_idx], fexpr, pos, wd, ht)
                r.draw_label(frame, fexpr, pos, wd, ht)
               #cv2.imshow('image',frames[f_idx])
                # red text
                fd.write("\n:" + str(count) +":" +str(fexpr_list[b_idx][0]) +":" +str(fexpr_list[b_idx][1]))

                print(count, "---------:" + str(fexpr_list[b_idx][0]) + ":" + str(fexpr_list[b_idx][1])+"\n")

                cv2.putText(frame, str(count), (10, 30), 0, 1, (0, 8, 255), 2)
        else:
                #white text (x,y) you should adjust by yourself
            cv2.putText(frame, str(count), (370, 30), 0, 1, (255, 255, 255), 2)

        if( count % 300 == 0 ):
            End_localtime = time.asctime(time.localtime(time.time()))
            print("---every 300 frame time : Final counter:", End_localtime, count)
            fd.write("\n" + "Ending time :" + End_localtime)
        # cv2.putText(frame, str(count), (550, 30), 0, 1, (255, 255, 255), 2)
        cv2.imshow('image',frame)
        #cv2.imwrite("./data/demo"+str(f_idx)+".png",frames[f_idx])
        
        #    cv2.waitKey(0)
        if cv2.waitKey(1)& 0xff == ord('q'):
              #print("-----------count:", count)
              break
        count = count + 1

        #cv2.imwrite("./data/demo"+str(1)+".png",frame)
#            cv2.imwrite("./data/GG.png",frames[b_idx])
    End_localtime = time.asctime(time.localtime(time.time()))
    print("---Ending time : Final counter:", End_localtime , count)
    fd.write("\n" + "Ending time :" + End_localtime)

    cap.release()
    cv2.destroyAllWindows()

    fd.close()
    


