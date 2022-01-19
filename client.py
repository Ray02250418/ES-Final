import socket, pickle, struct
import numpy as np
import cv2
from inference import detection_model

# create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.50.86'  # paste your server ip address here
port = 9999
client_socket.connect((host_ip, port))  # a tuple
data = b""
payload_size = struct.calcsize("Q") # Q: unsigned long long integer(8 bytes)

# create inference model
model = detection_model('Sample_TFLite_model', 0.5)

# open another branch to fix this (show image)
def inference_frame(frame, model):
    # inference
    # Loop over all detections and draw detection box if confidence is above minimum threshold
    for i in range(len(scores)):
        if ((scores[i] > model.min_conf_threshold) and (scores[i] <= 1.0)):

            # Get bounding box coordinates and draw box
            # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
            ymin = int(max(1,(boxes[i][0] * model.imH)))
            xmin = int(max(1,(boxes[i][1] * model.imW)))
            ymax = int(min(model.imH,(boxes[i][2] * model.imH)))
            xmax = int(min(model.imW,(boxes[i][3] * model.imW)))
            
            cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (10, 255, 0), 2)

            # Draw label
            object_name = model.labels[int(classes[i])] # Look up object name from "labels" array using class index
            label = '%s: %d%%' % (object_name, int(scores[i]*100)) # Example: 'person: 72%'
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
            label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
            cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
            cv2.putText(frame, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text

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

    (boxes, classes, scores, labels) = model.inference(frame) # inference model
    print('--------------------------------------------------------------------------------------------------')
    print(' '*100,labels)
    #inference_frame(frame, model)

    cv2.imshow("RECEIVING VIDEO", frame) # show video frame at client side
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'): # press q to exit video
        break