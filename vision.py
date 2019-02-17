#!/usr/bin/env python3
from cscore import CameraServer, VideoSource, UsbCamera, MjpegServer
import cv2
from  detectgreentape import *
import time
from networktables import NetworkTables
from networktables import NetworkTablesInstance
import atexit 
import json
import numpy as np

configFile = "/boot/frc.json"

class CameraConfig: pass

def FonctionSortie(capture, server, camera):
    print(type(capture))
    # capture.release()
    del server 
    del camera



def main():
    
    NetworkTables.initialize("10.68.51.2")
    
    
    LineDetect = DetectGreenTape()
    value = 0
    sd = NetworkTables.getTable("SmartDashboard")
    ntinst = NetworkTablesInstance.getDefault()
    ntinst.startServer()
    
    inst = CameraServer.getInstance()
    camera1 = UsbCamera("Camera1","/dev/v4l/by-path/platform-3f980000.usb-usb-0:1.2:1.0-video-index0" )
    camera2 = UsbCamera("Camera2","/dev/v4l/by-path/platform-3f980000.usb-usb-0:1.1.3:1.0-video-index0" )
    camera1.setConnectionStrategy(VideoSource.ConnectionStrategy.kKeepOpen)
    camera2.setConnectionStrategy(VideoSource.ConnectionStrategy.kKeepOpen)
    
    
    usb1 = inst.startAutomaticCapture(camera=camera1)
    usb2 = inst.startAutomaticCapture(camera=camera2)
    usb1.setResolution(320,240)
    usb2.setResolution(320,240)    
    cvSink = inst.getVideo(camera=camera2)
    img = np.zeros(shape=(240,320,3), dtype=np.uint8)
    while True:
        timestamp, img = cvSink.grabFrame(img)
        LineDetect.process(img)
        sd.putNumber('NbLinesDetectedNew',len(LineDetect.filter_lines_output))
        time.sleep(0.1)
        
    #capture.release()
    #cv2.findContours()

if __name__ == "__main__":
    main()