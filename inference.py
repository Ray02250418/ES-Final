# Import packages
import os
import cv2
import numpy as np
from threading import Thread

import subprocess as sp
import numpy
import queue
from tensorflow.lite.python.interpreter import Interpreter

class detection_model():
    def __init__(self, model_dir, min_conf_threshold):
        # load model
        self.freq = cv2.getTickFrequency()
        self.modeldir = model_dir
        self.graph_name = 'detect.tflite'
        self.label_name = 'labelmap.txt'
        self.min_conf_threshold = min_conf_threshold
        self.imW = 1280
        self.imH = 720

        #Get path to current working directory
        CWD_PATH = os.getcwd()
        # Path to .tflite file, which contains the model that is used for object detection
        PATH_TO_CKPT = os.path.join(CWD_PATH,self.modeldir,self.graph_name)
        # Path to label map file
        PATH_TO_LABELS = os.path.join(CWD_PATH,self.modeldir,self.label_name)

        # Load the label map
        with open(PATH_TO_LABELS, 'r') as f:
            self.labels = [line.strip() for line in f.readlines()]
        # Have to do a weird fix for label map if using the COCO "starter model" from
        # https://www.tensorflow.org/lite/models/object_detection/overview
        # First label is '???', which has to be removed.
        if self.labels[0] == '???':
            del(self.labels[0])

        # Load the Tensorflow Lite model.
        self.interpreter = Interpreter(model_path=PATH_TO_CKPT)
        self.interpreter.allocate_tensors()

        # Get model details
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.height = self.input_details[0]['shape'][1]
        self.width = self.input_details[0]['shape'][2]
        self.floating_model = (self.input_details[0]['dtype'] == np.float32) # False
        self.input_mean = 127.5
        self.input_std = 127.5
        self.targets = ['person', 'bicycle', 'car', 'motorcycle', 'bus', 'truck', 'cat', 'dog']

    def inference(self, input_frame): # return (boxes, classes, scores)
        # Acquire frame and resize to expected shape [1xHxWx3]
        frame = input_frame.copy()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (self.width, self.height))
        input_data = np.expand_dims(frame_resized, axis=0)

        # Perform the actual detection by running the model with the image as input
        self.interpreter.set_tensor(self.input_details[0]['index'],input_data)
        self.interpreter.invoke()

        # Retrieve detection results
        boxes = self.interpreter.get_tensor(self.output_details[0]['index'])[0] # Bounding box coordinates of detected objects
        classes = self.interpreter.get_tensor(self.output_details[1]['index'])[0] # Class index of detected objects
        scores = self.interpreter.get_tensor(self.output_details[2]['index'])[0] # Confidence of detected objects
        labels=[]
        for i in range(len(classes)):
            if (scores[i] >= self.min_conf_threshold) and (scores[i]<=1) and (self.labels[int(classes[i])] in self.targets):
                labels.append(self.labels[int(classes[i])])

        return (boxes, classes, scores, labels)

