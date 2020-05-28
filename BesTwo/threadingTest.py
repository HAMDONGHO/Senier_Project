import logging
import threading
import time
import datetime
import picamera
import keyboard
import cv2
camera = picamera.PiCamera()
savepath = '/home/pi/bestwo/python3/savedVideo'

def thread_function(name):
    now = time.strftime('%H-%M-%s',time.localtime(time.time()))
    print(now)
    camera.start_recording(output = savepath + '/video' +now+ '.h264')
    camera.start_preview(fullscreen=False, window=(100,20,640,480))
    while True:
        nowsec=time.strftime('%S', time.localtime(time.time()))
        print(nowsec)
        time.sleep(1)
        if nowsec=='55':
            break
    camera.stop_preview()
    camera.stop_recording()
    #1st recording trial done. and a loop starts
    
    while True:
        now = time.strftime('%H-%M-%s',time.localtime(time.time()))
        while True:
            nowsec=time.strftime('%S', time.localtime(time.time()))
            print(nowsec)
            time.sleep(1)
            if nowsec=='00':
                break
        camera.start_recording(output = savepath + '/video' +now+ '.h264')
        camera.start_preview(fullscreen=False, window=(100,20,640,480))
        while True:
            nowsec=time.strftime('%S', time.localtime(time.time()))
            print(nowsec)
            time.sleep(0.5)
            if nowsec=='55':
                break
        camera.stop_preview()
        camera.stop_recording()
    
##    while True:
##        now = time.strftime('%H-%M-%s',time.localtime(time.time()))
##        nowsec=time.strftime('%S', time.localtime(time.time()))
##        print("Thread %s: starting", name)
##        camera.start_recording(output = savepath + '/video' +now+ '.h264')
##        camera.start_preview(fullscreen=False, window=(100,20,640,480))  
##        camera.wait_recording(20)
##        print("Thread %s: finishing", name)
##        camera.stop_preview()
##        camera.stop_recording()


def CameraOn():
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format,level=logging.INFO,datefmt="%H:%M:%S")
    print("Main    : before creating thread")
    x = threading.Thread(target=thread_function, args=(1,))
    current=1
    print("Main    : before running thread")
    x.start()
    print("Main    : wait for the thread to finish")
##        x.join()
    print("Main    : all done")
