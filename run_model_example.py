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
import asyncio
import websockets

camera1 = ObjectDetectionCamera('picamera1', 'Sample_TFLite_model', 0.6)
camera2 = ObjectDetectionCamera('picamera2', 'Sample_TFLite_model', 0.6)

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
async def hello(websocket):
    name = await websocket.recv()
    camera_num = f"{name}"

    danger_state = '0'
    if camera_num == '1':
        if camera1.get_danger_state():
            danger_state='1'
        else:
            danger_state='0'
    elif camera_num == '2':
        if camera2.get_danger_state():
            danger_state='1'
        else:
            danger_state='0'
    else:
        print("Invalid input from STM (must be 1 or 2)")

    await websocket.send(danger_state)
    print(f"send danger state to camera {camera_num} >> {danger_state}")

async def main():
    async with websockets.serve(hello, "localhost", 8001):
        await asyncio.Future()  # run forever

asyncio.run(main())

# Clean up
cv2.destroyAllWindows()
#videostream.stop()
