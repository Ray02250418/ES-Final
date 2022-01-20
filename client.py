from camera import Camera
from multiprocess import Process, Value 
from threading import Thread

def setup_camera0(danger):
    camera0 = Camera('192.168.50.243', 5555, 0)
    camera0.detect(danger)
    
def setup_camera1(danger):
    camera1 = Camera('192.168.50.86', 8889, 1)
    camera1.detect(danger)
    
if __name__ == '__main__':
    # camera0 = Camera('192.168.50.243', 5555, 0)
    # camera1 = Camera('192.168.50.86', 8889, 1)
    left_danger = Value('i', 0)
    right_danger = Value('i', 0)
    Left = Process(target=setup_camera0, args=[left_danger])
    Right = Process(target=setup_camera1, args=[right_danger])
    Left.start()
    Right.start()
    
    
    # left_danger = 0
    # setup_camera(left_danger, '192.168.50.243', 5555, 0)
    
    