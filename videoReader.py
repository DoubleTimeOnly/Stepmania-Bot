import cv2

def VideoPlayer(video):
    frame = 0
    while True:
        try:
            image = video[frame]
        except IndexError:
            print "invalid frame"
        cv2.imshow('video', image)
        print "f: %d of %d" %(frame,len(video))
        key = cv2.waitKey(1)
        if key & 0xFF == ord('r'):
            frame +=1
        if key & 0xFF == ord('e'):
            frame -=1
        if key & 0xFF == ord('j'):
            try:
                frame = int(raw_input("Enter frame number: "))
            except:
                print "invalid number"
        if key & 0xFF == ord('q'):
            print '[Exiting player]'
            video = []
            return
