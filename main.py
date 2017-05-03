'''
note: somehow stepmania cuts fps down from 55 to 30
'''

import imutils      #basic image editing
import numpy
import cv2
from PIL import Image,ImageGrab
from matplotlib import pyplot
import time
from DirectKeys import PressKey,ReleaseKey,UP,DOWN,LEFT,RIGHT
from videoReader import VideoPlayer
def ColorMask(image,lowerBoundary,upperBoundary):
    
    lower = numpy.array(lowerBoundary,dtype='uint8')
    upper = numpy.array(upperBoundary,dtype='uint8')
    
    mask = cv2.inRange(image,lower,upper)
    return mask
    #return cv2.bitwise_and(image,image,mask=mask)
from video_capture2 import CaptureScreen

def main():
    ############
    ##Settings##
    ############
    inputOn = True
    screenOn = False
    noteType='bar'  #options: bar | arrow
     
    
    ###############
    ##Calibration##
    ###############
    #Current settings for ~30 fps
    #c500:30 | c200:15 | c150:10
    threshold = 30      #how early notes can be hit
    minThreshold = 15   #how late notes can be hit
    base = 52           #exactly where receptors are
    
    ##delay lays somewhere between (0.02,0.5)
    ##idk tbh
    #delay = 0.04
    delay = 0.002   #minimum time between arrow presses
    
    #############
    ##Constants##
    #############
    #mark middle of note from top
    #lrHeight is left,right notes and udHeight is up,down notes
    if noteType=='arrow':
        lrHeight=30
        udHeight=30
    if noteType=='bar':
        lrHeight=13
        udHeight=13       
    #Define lower and upper range of what is considered that color
    #lower,upper BGR format
    red = ([0, 0, 150], [130, 130, 255],'red') 
    yellow = ([0, 160, 160], [50, 255, 255],'yellow') 
    blue = ([100, 0, 0], [250, 56, 50],'blue')
    colors = [red]      #which colors will be looked for
    video = []      #if screenOn=True, stores each frame of screen, clears at 5000 frames
    count = 0
    avgFPS=0    
    tUP = 0
    tLEFT = 0
    tRIGHT = 0
    tDOWN = 0
    
    ##Print settings
    print '[Notetype]:',noteType
    print '[Colors]: ',colors
    print '[Threshold]:',threshold
    print '[Min-Threshold]:',minThreshold
    while(True):
        tInitial = time.time()
        
        ##Input format: (width,height),(cornerX,cornerY)
        screen = CaptureScreen((300,150),(1340,94))     
       
        screen = cv2.cvtColor(screen, cv2.COLOR_RGBA2RGB)  #remove alpha channel        
        contours = []
        
        ##mask the screen over the selected colors to find arrows of said colors
        ##and store each contour(arrow) in a list
        for color in colors:
            #masked_data = ColorMask(screen,color[0],color[1])
            frameDelta = ColorMask(screen,color[0],color[1])
            #cv2.imshow('%s' %(color[2]),masked_data)
            #cv2.waitKey(1)      
            #frameDelta = cv2.absdiff(background, masked_data) #was masked_data
            #cv2.imshow('diff',frameDelta)
            
            #frameDelta = cv2.cvtColor(frameDelta, cv2.COLOR_BGR2GRAY) 

            (c1,contoursTemp,c2) = cv2.findContours(frameDelta, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)     
            contours.extend(contoursTemp)
        
        ##Hitbox drawing
        cv2.line(screen, (0,base),(300,base), (255,0,0),2)    #receptor hitbox
        #min-threshold lines
        cv2.line(screen, (0,base-29-minThreshold),(500,base-29-minThreshold), (0,0,255),1)
        cv2.line(screen, (0,base-13-minThreshold),(500,base-13-minThreshold), (0,0,255),1)
        #max-threshold line
        cv2.line(screen, (0,base+threshold),(300,base+threshold), (125,125,0),1)    #receptor hitbox
        #Lane lines
        cv2.line(screen, (47,0),(47,200), (255,0,0),1)
        cv2.line(screen, (111,0),(111,200), (255,0,0),1)
        cv2.line(screen, (175,0),(175,200), (255,0,0),1)
        cv2.line(screen, (240,0),(240,200), (255,0,0),1)                  
        
        #################
        ##Hit Detection##
        #################
        for cnt in contours:
            ##make sure we're not picking up some random contour
            if cv2.contourArea( cnt ) > 20:
                ##bounding rectangle: rectangle that encompasses contour
                ##x,y is top left coord, w,h is width and height
                x,y,w,h = cv2.boundingRect(cnt)

                ##calculate X position of arrow
                moments = cv2.moments(cnt)   
                cx = int(moments['m10']/moments['m00'])
                
                ##calculate y position of arrow
                cy = y+30                
                
                if (cx < 47+31 and cx > 47-31) or (cx < 240+31 and cx > 240-31):
                    cy = y+lrHeight     #determine note's hitbox
                    if y <= base-lrHeight-minThreshold:    #check not too far up
                        continue                    
                elif (cx < 111+31 and cx > 111-31) or (cx < 175+31 and cx > 175-31):
                    if y < base-udHeight-minThreshold:
                        continue
                    cy = y+udHeight
                
                ##outlines arrow and draws boxes around them
                ##just for visual purposes
                cv2.rectangle(screen,(x,y),(x+w,y+h),(0,255,0),1)
                #cv2.drawContours(screen, [cnt],-1, (0, 255, 0), 1)                
                ##draw arrow's "hitline" in light blue
                cv2.line(screen, (x,cy),(x+w,cy), (255,255,0),2)
                
                ##if the arrow is within threshold pixels of the target
                ##then press the appropriate key
                if cy < base+threshold and cy > base-threshold-5 and inputOn:
                    if cx < 47+31 and cx > 47-31:
                        #notes cannot be pressed twice within "delay" seconds
                        if tInitial - tLEFT < delay:
                            continue
                        tLEFT = time.time()     #reset input timer
                        PressKey(LEFT)
                        cv2.line(screen, (x,cy),(x+w,cy), (0,255,255),2)
                        ReleaseKey(LEFT)
                        
                    if cx < 111+31 and cx > 111-31:
                        if tInitial - tDOWN < delay:
                            continue        
                        tDOWN = time.time()                        
                        PressKey(DOWN)
                        cv2.line(screen, (x,cy),(x+w,cy), (0,255,255),2)
                        ReleaseKey(DOWN)
                    if cx < 175+31 and cx > 175-31:
                        if tInitial - tUP < delay:
                            continue        
                        tUP = time.time()                         
                        PressKey(UP)
                        cv2.line(screen, (x,cy),(x+w,cy), (0,255,255),2)
                        ReleaseKey(UP)     
                    if cx < 240+31 and cx > 240-31:
                        if tInitial - tRIGHT < delay:
                            continue        
                        tRIGHT = time.time()                         
                        PressKey(RIGHT)
                        cv2.line(screen, (x,cy),(x+w,cy), (0,255,255),2)
                        ReleaseKey(RIGHT)
        ###############
        ##Scren Stuff##
        ###############
        if screenOn:
            cv2.imshow('temp',screen)
            if len(video) > 5000:   #clear buffer if contents are too large
                video = []
            video.append( cv2.cvtColor(screen,cv2.COLOR_RGB2GRAY))  #save some space
            key = cv2.waitKey(1)
    
            if key & 0xFF == ord('p'):
                print 'paused'
                while True:
                    key = cv2.waitKey(0)
                    if key & 0xFF == ord('r'):                
                        print 'resume'
                        break
                    if key & 0xFF == ord('v'):
                        VideoPlayer(video)
        tFinal = time.time()
        
        ##prints fps every 20 cycles
        if count == 20:
            print '[average fps]',1/(avgFPS/20)
            count = 0
            avgFPS = 0
        count += 1
        avgFPS += tFinal - tInitial
if __name__ == '__main__':
    main()

        