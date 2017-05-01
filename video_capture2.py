import numpy
import cv2
import time
import win32gui, win32ui, win32con, win32api
#1060,40,1920,520
def CaptureScreen():
    hwin = win32gui.GetDesktopWindow()
    height = 480
    width = 860
    left = 1060
    top = 40
    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
    
    signedIntsArray = bmp.GetBitmapBits(True)
    img = numpy.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height,width,4)
    
    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())
    
    return img


if __name__ == '__main__':
    img = CaptureScreen()
    img = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
    
    cv2.imshow('temp',img)
    cv2.waitKey(0)    