import os
import cv2
import tensorflow as tf


import resnet as r
import logging
from nets import resnet_v2
from preprocessing import inception_preprocessing


class EmotionClassifier():
    def __init__(self):
        slim = tf.contrib.slim
        CLASSES = ['anger', ' happy ', 'neutral', ' sad ', 'surprise']

        image_size = 160
        checkpoints_dir = 'models/inception_5/'

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



if __name__ == "__main__":
    emoC1 = EmotionClassifier()

    #emotionclassifier1.__init__()
    #frame = cv2.imread('data/456.jpg')

    #breakupTeacherStudent.mp4')#Marquess-Vayamos.avi')#news_kp_partial.mp4#456.jpg
    ret, frame = cv2.VideoCapture('data/456.jpg').read()
    bbox_list = [(1096, 618, 26, 32), (814, 550, 35, 33), (998, 145, 65, 87), (65, 142, 67, 77), (313, 75, 73, 95)]

    #fexpr_list = r.classify_image(frame, bbox_list)
    fexpr_list = r.classify_image(emoC1.sess, emoC1.image, emoC1.processed_image, emoC1.processed_images, emoC1.probs, emoC1.logger,frame, bbox_list)

    print(fexpr_list)

    for idx,bbox in enumerate(bbox_list):#range(len(bbox_list)):ro

        #bbox = bbox_list[idx]
        pos = (bbox[0], bbox[1])
        wd = bbox[2]
        ht = bbox[3]

        fexpr = fexpr_list[idx][0]

        r.draw_label(frame, fexpr, pos, wd, ht)

    cv2.imshow('image',frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
