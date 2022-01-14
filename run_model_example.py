# Import packages
import os
import argparse
import cv2
import numpy as np
from threading import Thread
import importlib.util
import socket

import subprocess as sp
import queue
from ObjectDetectionCamera import ObjectDetectionCamera
import asyncio
import websockets

camera1 = ObjectDetectionCamera('picamera1', 'Sample_TFLite_model', 0.6) # 192.168.50.86
camera2 = ObjectDetectionCamera('picamera2', 'Sample_TFLite_model', 0.6) # 192.168.50.243

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
    # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
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
    print(danger_state)

    await websocket.send(danger_state)
    print(f"send danger state to camera {camera_num} >> {danger_state}")

async def main():
    async with websockets.serve(hello, "localhost", 8000):
        await asyncio.Future()  # run forever

def stm_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        HOST="140.112.151.152"
        PORT=8000
        s.bind((HOST, PORT))
        s.listen(0)
        while True:
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print()
                while True:
                    data = conn.recv(1024).decode('utf-8')
                    
                    danger_state_1 = '0'
                    danger_state_2 = '0'
                    if camera1.get_danger_state():
                        danger_state_1='1'
                    else:
                        danger_state_1='0'
                    if camera2.get_danger_state():
                        danger_state_2='1'
                    else:
                        danger_state_2='0'

                    return_msg = danger_state_1+danger_state_2
                    conn.send(return_msg.encode('utf-8'))
                    print('Responsed from socket server : ', return_msg)


server_num=1
if server_num==1:
    stm_server_thread = Thread(target=stm_server) 
    stm_server_thread.start()
else:
    asyncio.run(main())

# Clean up
cv2.destroyAllWindows()
#videostream.stop()
