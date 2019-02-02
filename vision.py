#!/usr/bin/env python3
from cscore import CameraServer, VideoSource, UsbCamera, MjpegServer
import cv2
from  detectgreentape import *
import time
from networktables import NetworkTables
from networktables import NetworkTablesInstance
import atexit 


def FonctionSortie(capture, server, camera):
    print(type(capture))
    capture.release()
    del server 
    del camera


def main():
    
    NetworkTables.initialize("10.68.51.2")
    capture = cv2.VideoCapture("/dev/v4l/by-path/platform-3f980000.usb-usb-0:1.1.3:1.0-video-index0")
    
    
    LineDetect = DetectGreenTape()
    value = 0
    sd = NetworkTables.getTable("SmartDashboard")
    ntinst = NetworkTablesInstance.getDefault()
    ntinst.startServer()
    inst = CameraServer.getInstance()
    camera = UsbCamera("Camera1","/dev/v4l/by-path/platform-3f980000.usb-usb-0:1.2:1.0-video-index0" )
    server = inst.startAutomaticCapture(camera=camera, return_server=True)
    atexit.register(FonctionSortie, capture, server, camera)
    while True:
        
        ret, frame = capture.read()
        if ret:
            LineDetect.process(frame)
            sd.putNumber('NbLinesDEtected',len(LineDetect.filter_lines_output))    
        #time.sleep(0.1)
        
        
        
        
        #print ("done")
        #cv2.imshow('frame',frame)
        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break
    #capture.release()
    #cv2.findContours()

if __name__ == "__main__":
    main()