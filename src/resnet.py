import cv2
import numpy as np
import tensorflow as tf
import time
import json
 
slim = tf.contrib.slim
CLASSES = ['anger', ' happy ', 'neutral', ' sad ', 'surprise']


def draw_label(image, label, pos, wd, ht):
    left_top = pos
    right_bot = (pos[0]+wd, pos[1]+ht)
    color = (0, 255, 0)
    thickness = 3
    cv2.rectangle(image, left_top, right_bot, color, thickness)


    offset = 20
    left_top = (pos[0], pos[1]-offset)
    text = CLASSES[label]
    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (128, 255, 255)
    font_scale = 0.9
    line_type = 2
    cv2.putText(image, text, left_top, font, font_scale, color, line_type)


def classify_image(sess, image, processed_image, processed_images, probs,logger, frame, bbox_list):

    fexpr_list = []    
    face_list = []

    for bbox in bbox_list:
        x = int(bbox[0])
        y = int(bbox[1])
        wd = int(bbox[2])
        ht = int(bbox[3])

        # image preprocessing
        roi = frame[y:y+ht, x:x+wd]
        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
        roi = sess.run(processed_image, feed_dict={image: roi})
        face_list.append(roi)
 
    stime = time.time()
    # classify
    if 0 != len(face_list):
        face_images = np.array(face_list)
        probabilities = sess.run(probs,feed_dict={processed_images: face_images})
        labels = np.argmax(probabilities, 1)        
        #fexpr_list = labels.tolist()
        maxprobabilities = np.amax(probabilities, 1)
        fexpr_list = [v for v in zip(labels, maxprobabilities)]
        assert len(bbox_list) == len(fexpr_list)
        my_json_string = '[{'
        for idx in range(len(bbox_list)):
            x = int(bbox_list[idx][0])
            y = int(bbox_list[idx][1])
            wd = int(bbox_list[idx][2])
            ht = int(bbox_list[idx][3])
            emotion = probabilities[idx]
            json_string = json.dumps(
               {'faceRectangle':{
                   'x': x,
                   'y': y,
                   'wd': wd,
                   'ht':ht}, 
                'scores':{
                   CLASSES[0]:float(emotion[0]),
                   CLASSES[1]:float(emotion[1]),
                   CLASSES[2]:float(emotion[2]),
                   CLASSES[3]:float(emotion[3]),
                   CLASSES[4]:float(emotion[4])}})
            logger.info(json_string)
    etime = time.time()
    logger.info('classified frame with time {:.06f} sec'.format(etime-stime))

    return fexpr_list  

