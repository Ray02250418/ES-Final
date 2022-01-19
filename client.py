from camera import Camera
from multiprocessing import Process
from threading import Thread

if __name__ == '__main__':
    camera0 = Camera('192.168.50.243', 5555, 0)
    camera1 = Camera('192.168.50.86', 8889, 1)
    Left = Thread(target=camera0.detect)
    Right = Thread(target=camera1.detect)
    Left.start()
    Right.start()
    
    