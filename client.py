from camera import Camera
import multiprocessing as mp
from threading import Thread

if __name__ == '__main__':
    camera0 = Camera('192.168.50.243', 5555, 0)
    camera1 = Camera('192.168.50.86', 8889, 1)
    Left = mp.Process(target=camera0.detect)
    Right = mp.Process(target=camera1.detect)
    Left.start()
    Right.start()
    
    Left.join()
    Right.join()
    