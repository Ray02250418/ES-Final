# Import packages
import os
import argparse
import cv2
import numpy as np
from threading import Thread
import importlib.util

import subprocess as sp
import queue
from ObjectDetectionCamera import ObjectDetectionCamera

camera1 = ObjectDetectionCamera('picamera1', 'Sample_TFLite_model')
camera2 = ObjectDetectionCamera('picamera2', 'Sample_TFLite_model')

cam1_get_frame = Thread(target=camera1.get_frame)
cam1_get_frame.start()
cam1_display = Thread(target=camera1.display)
cam1_display.start()

cam2_get_frame = Thread(target=camera2.get_frame)
cam2_get_frame.start()
cam2_display = Thread(target=camera2.display)
cam2_display.start()

# Send new deteced_queue to STM (HTTP server, ws server) each time queue is updated
# through POST '/'

# Clean up
cv2.destroyAllWindows()
#videostream.stop()
