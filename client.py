import socket, pickle, struct
import numpy as np
import cv2
from inference import detection_model

# create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.50.86'  # paste your server ip address here
port = 9997
client_socket.connect((host_ip, port))  # a tuple
data = b""
payload_size = struct.calcsize("Q") # Q: unsigned long long integer(8 bytes)

# create inference model
model = detection_model('Sample_TFLite_model', 0.5)

#Business logic to receive data frames, and unpak it and de-serialize it and show video frame on client side
while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4 * 1024)  # 4K, range(1024 byte to 64KB)
        if not packet: break
        data += packet # append the data packet got from server into data variable
    packed_msg_size = data[:payload_size] #will find the packed message size i.e. 8 byte, we packed on server side.
    data = data[payload_size:] # Actual frame data
    msg_size = struct.unpack("Q", packed_msg_size)[0] # meassage size
    
    while len(data) < msg_size:
        data += client_socket.recv(4 * 1024) # will receive all frame data from client socket
    frame_data = data[:msg_size] #recover actual frame data
    data = data[msg_size:]
    frame = pickle.loads(frame_data) # de-serialize bytes into actual frame type

    (boxes, classes, scores) = model.inference(frame) # inference model
    print('---------------------------------')
    print(classes)

    cv2.imshow("RECEIVING VIDEO", frame) # show video frame at client side
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'): # press q to exit video
        break