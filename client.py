from camera import Camera
from multiprocess import Process, Value 
from threading import Thread
import socket

def setup_camera0(danger, sent):
    camera0 = Camera('192.168.50.243', 5555, 0, 0.6)
    camera0.detect(danger, sent)
    
def setup_camera1(danger, sent):
    camera1 = Camera('192.168.50.86', 8888, 1, 0.6)
    camera1.detect(danger, sent)
    
def stm_server(danger_left, danger_right, left_sent, right_sent):
    print("Start STM server")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        HOST="140.112.71.131"
        PORT=15001
        s.bind((HOST, PORT))
        s.listen(0)
        while True:
            print("Waiting for connection!")
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print()
                while True:
                    data = conn.recv(1024).decode('utf-8')
                    print(data)
                    danger_state_1 = '0'
                    danger_state_2 = '0'
                    print('danger_left: ', danger_left.value)
                    print('danger_right: ', danger_right.value)
                    if danger_left.value==1:
                        danger_state_1='1'
                    else:
                        danger_state_1='0'
                    if danger_right.value==1:
                        danger_state_2='1'
                    else:
                        danger_state_2='0'

                    return_msg = danger_state_2+danger_state_1
                    print(return_msg)
                    conn.send(return_msg.encode('utf-8'))
                    left_sent.value = 1
                    right_sent.value = 1
                    #print('Responsed from socket server : ', return_msg)
    
if __name__ == '__main__':
    # camera0 = Camera('192.168.50.243', 5555, 0)
    # camera1 = Camera('192.168.50.86', 8889, 1)
    left_danger = Value('i', 0)
    left_sent = Value('i', 1)
    right_danger = Value('i', 0)
    right_sent = Value('i', 1)
    Left = Process(target=setup_camera0, args=[left_danger, left_sent])
    Right = Process(target=setup_camera1, args=[right_danger, right_sent])
    server = Process(target=stm_server, args=[left_danger, right_danger, left_sent, right_sent])
    Left.start()
    Right.start()
    server.start()

    
    
    # left_danger = 0
    # setup_camera(left_danger, '192.168.50.243', 5555, 0)
    
    