import socket, pickle, struct
import numpy as np
import cv2
from inference import detection_model

class Camera():
    def __init__(self, ip, port, num, conf_threshold):
        # create socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((ip, port))  # a tuple
        self.data = b""
        self.payload_size = struct.calcsize("Q") # Q: unsigned long long integer(8 bytes)
        self.num = num

        # create inference self.model
        self.model = detection_model('Sample_TFLite_model', conf_threshold)

    def detect(self, danger):
        #Business logic to receive self.data frames, and unpak it and de-serialize it and show video frame on client side
        while True:
            while len(self.data) < self.payload_size:
                packet = self.client_socket.recv(4 * 1024)  # 4K, range(1024 byte to 64KB)
                if not packet: break
                self.data += packet # append the self.data packet got from server into self.data variable
            packed_msg_size = self.data[:self.payload_size] #will find the packed message size i.e. 8 byte, we packed on server side.
            self.data = self.data[self.payload_size:] # Actual frame self.data
            msg_size = struct.unpack("Q", packed_msg_size)[0] # meassage size
            
            while len(self.data) < msg_size:
                self.data += self.client_socket.recv(4 * 1024) # will receive all frame self.data from client socket
            frame_data = self.data[:msg_size] #recover actual frame self.data
            self.data = self.data[msg_size:]
            frame = pickle.loads(frame_data) # de-serialize bytes into actual frame type

            (boxes, classes, scores, labels) = self.model.inference(frame) # inference self.model
            print('------------------------------------------------------------------------')
            print(' ' * self.num * 100, self.num, ': ', labels)
            #inference_frame(frame, self.model)
            
            if len(labels)>0:
                danger=1
            else:
                danger=0

            # cv2.imshow("RECEIVING VIDEO", frame) # show video frame at client side
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'): # press q to exit video
                break