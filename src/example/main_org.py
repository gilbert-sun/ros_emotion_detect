import cv2
#import resnet as r
import tensorflow as tf

# if __name__ == "__main__":
#
#     frame = cv2.imread('data/456.jpg')
#     bbox_list = [(1096, 618, 26, 32), (814, 550, 35, 33), (998, 145, 65, 87), (65, 142, 67, 77), (313, 75, 73, 95)]
#
#     #frame = cv2.imread('data/123.jpg')
#     #bbox_list = [(580, 101, 438, 502)]
#
#     #frame = cv2.imread('data/789.jpg')
#     #bbox_list = [(856, 237, 90, 107), (496, 208, 85, 106)]
#
#     fexpr_list = r.classify_image(frame, bbox_list)
#     print(fexpr_list)
#
#     for idx in range(len(bbox_list)):
#
#         bbox = bbox_list[idx]
#
#         pos = (bbox[0], bbox[1])
#         wd = bbox[2]
#         ht = bbox[3]
#         fexpr = fexpr_list[idx][0]
#
#         r.draw_label(frame, fexpr, pos, wd, ht)
#
#     cv2.imshow('image',frame)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

if __name__ == "__main__":

    # frame = cv2.imread('data/456.jpg')
    # bbox_list = [(1096, 618, 26, 32), (814, 550, 35, 33), (998, 145, 65, 87), (65, 142, 67, 77), (313, 75, 73, 95)]

    face_cascade = cv2.CascadeClassifier('./cascades/haarcascade_frontalface_default.xml')
    frame = cv2.imread("./face1.jpg")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5, )

    bbox_list = [(x,y,w,h) for (x,y,w,h) in faces ]
    print( "\n\n-----------\n", bbox_list  )


    #frame = cv2.imread('data/123.jpg')
    #bbox_list = [(580, 101, 438, 502)]

    # frame = cv2.imread('data/789.jpg')
    # bbox_list = [(856, 237, 90, 107), (496, 208, 85, 106)]

    #fexpr_list = r.classify_image(frame, bbox_list)


    for idx in range(len(bbox_list)):

        bbox = bbox_list[idx]

        pos = (bbox[0], bbox[1])
        wd = bbox[2]
        ht = bbox[3]
        # fexpr = fexpr_list[idx]
        #fexpr = fexpr_list[idx][0]
        print ('----', bbox_list[idx], "===", idx)#, fexpr_list[idx])
        #r.draw_label(frame, fexpr, pos, wd, ht)

    cv2.imshow('image',frame)

    cv2.imwrite("./demo11.jpg", frame)
    # cv2.imwrite("./data/demo.jgp",frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()






