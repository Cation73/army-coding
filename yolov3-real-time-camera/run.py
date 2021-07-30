# -*- coding: utf-8 -*-


import cv2
import numpy as np

from yolov3 import YoloV3, load_darknet_weights, preprocess_image, draw_outputs


# define values which we will use later
yolo_iou_threshold   = 0.6 # iou threshold
yolo_score_threshold = 0.8 # score threshold

weightsyolov3 = 'E:/yolov3.weights' # path to weights file
weights= 'checkpoints/yolov3.tf' # path to checkpoints file
size= 416             # resize images to
checkpoints = 'checkpoints/yolov3.tf'
num_classes = 80      # number of classes in the model

# define model
yolo = YoloV3(classes=num_classes)

load_darknet_weights(yolo, weightsyolov3)

yolo.save_weights(checkpoints)

class_names =  ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck",
  "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench",
  "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe",
  "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard",
  "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard",
  "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl",
  "banana","apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut",
  "cake","chair", "sofa", "pottedplant", "bed", "diningtable", "toilet", "tvmonitor", "laptop",
  "mouse","remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink",
  "refrigerator","book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"]

# turn on the camera
cap = cv2.VideoCapture(0)
while True:
    # read frame from camera
    ret, image_np = cap.read()
    # reshape for input image
    inp_img_size = image_np.shape[:2] # hw
    # resize input image_np to normal size
    image_inp = cv2.resize(image_np, (size, size))
    # preprocess image for input model
    image_prep = preprocess_image(np.expand_dims(image_inp, 0), size)
    boxes, scores, classes, nums = yolo(image_prep)
    print(boxes)
    print()
    print(classes)
    # draw output image
    res_image = draw_outputs(image_inp, (boxes, scores, classes, nums), class_names)
    res_image = cv2.resize(res_image, (inp_img_size[1], inp_img_size[0]))
    # Display output
    cv2.imshow('object detection', res_image)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()