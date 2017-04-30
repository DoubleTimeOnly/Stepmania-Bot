'''
note: cmod 50 seems optimal atm
'''

import imutils      #basic image editing
import numpy
import cv2
from PIL import Image,ImageGrab
from matplotlib import pyplot
import time
from DirectKeys import PressKey,ReleaseKey,UP,DOWN,LEFT,RIGHT
def mask(image):
    mask = numpy.zeros_like(image,numpy.uint8)
    mask = cv2.rectangle(mask, (300,55) , (560,350), 255, thickness=-1)
    masked_data = cv2.bitwise_and(image,image,mask = mask)    
    return masked_data
        

def main():
   
    count = 0
    avgFPS=0
    background = cv2.imread('background.png')
    background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY) 
    background = mask(background)
    edgedbackground = cv2.imread('edged_background.png')
    edgedbackground = cv2.cvtColor(edgedbackground, cv2.COLOR_BGR2GRAY) 
    edgedbackground = mask(edgedbackground)    
    temp = 0
    lastPressed=''
    lastProportional = 85
    threshold = 12
    integralSum = 0
    base = 85
    while(True):
        tInitial = time.time()
        printscreen_pil =  ImageGrab.grab(bbox=(1060,40,1920,520) )
        screen = numpy.array(printscreen_pil,dtype='uint8')#.reshape((printscreen_pil.size[1],printscreen_pil.size[0],3)) 
        gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY) 
        masked_data = mask(gray)

        
        #cv2.imshow('window',masked_data)
        #edged = cv2.Canny(masked_data, 300, 380)
        #cv2.imshow('edge',edged)

        frameDelta = cv2.absdiff(background, masked_data) #was masked_data
        #retval,frameDelta = cv2.threshold(frameDelta,40,255,cv2.THRESH_BINARY)
        cv2.imshow('diff',frameDelta)
        #try:
            #(contours, _) = cv2.findContours(frameDelta, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #except ValueError:
        (c1,contours,c2) = cv2.findContours(frameDelta, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)     
        
        cv2.line(screen, (300,85),(550,85), (255,0,0),2)
        #cv2.line(screen, (300,92),(550,92), (255,0,0),2)
        
        
        #left down up right
        #cv2.line(screen, (330,85),(330,200), (255,0,0),2)
        ##cv2.line(screen, (310,85),(310,200), (255,255,0),2)
        ##cv2.line(screen, (350,85),(350,200), (255,255,0),2)
        
        #cv2.line(screen, (395,85),(395,200), (255,0,0),2)
        #cv2.line(screen, (460,85),(460,200), (255,0,0),2)
        #cv2.line(screen, (525,85),(525,200), (255,0,0),2)
        
        if temp ==1:
            temp = 0
            
            for cnt in contours:
                if cv2.contourArea( cnt ) > 300:
                    x,y,w,h = cv2.boundingRect(cnt) #x,y is top left coord, w,h is width and height
                    #print x,y,w,h
                    cv2.rectangle(screen,(x,y),(x+w,y+h),(0,255,0),1)
                    cv2.drawContours(screen, [cnt],-1, (0, 255, 0), 1)
                    moments = cv2.moments(cnt)   
                    cx = int(moments['m10']/moments['m00'])
                    cy = int(moments['m01']/moments['m00'])
                    #print cy
                    
                    cy = y+30
                    cv2.line(screen, (300,cy),(550,cy), (0,0,255),2)
                    
                    ##pid threshold values?
    
                    if cy < 85+threshold and cy > 85-20:
                        cv2.line(screen, (300,cy),(550,cy), (0,255,255),2)                        
                        if cx < 330+20 and cx > 330-20:
                            lastPressed = 'left'
                            PressKey(LEFT)
                            ReleaseKey(LEFT)
                                
                        if cx < 395+20 and cx > 395-20:
                            lastPressed = 'down'
                            PressKey(DOWN)
                            ReleaseKey(DOWN)
                                
                        if cx < 460+20 and cx > 460-20:
                            lastPressed = 'up'
                            PressKey(UP)
                            ReleaseKey(UP)                                      
                                
                        if cx < 525+20 and cx > 525-20:
                            PressKey(RIGHT)
                            ReleaseKey(RIGHT)
        temp+=1
        cv2.imshow('temp',screen)
        

        #if cv2.waitKey(1) & 0xFF == ord('q'):
            #cv2.imwrite('background.png',masked_data)
            ##cv2.imwrite('edged_background.png',edged)    
            #print 'background frame updated'
            #return

        if cv2.waitKey(1) & 0xFF == ord('p'):
            print 'paused'
            while True:
                if cv2.waitKey(25) & 0xFF == ord('r'):
                    print 'resume'
                    break

        tFinal = time.time()
        if count == 20:
            print '[average fps]',1/(avgFPS/20)
            count = 0
            avgFPS = 0
        count +=1
        avgFPS += tFinal - tInitial
if __name__ == '__main__':
    main()