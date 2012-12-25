# Программа неподвижный фон видео, убирая движущиеся объекты

import cv2.cv as cv

HORIZONTAL_FLIP = 1 # Const horisontal flipping mode

"""    
    imgThreshed = cv.CreateImage(cv.GetSize(img), 8, 1);

    # Values 20,100,100 to 30,255,255 working perfect for yellow at around 6pm
    cv.InRangeS(imgHSV, cv.Scalar(112, 100, 100), cv.Scalar(124, 255, 255), imgThreshed);
    return imgThreshed;
"""

# Параметр, устойчивости фона
# 0 <= alpha <= 1
# Чем меньше, тем фон менее устойчив 
alpha = 0.94

capture = cv.CreateCameraCapture(0)

if(capture is None):
    print "Error: camera capture can't be create"
    exit()
    
backgroundWindow = 'Background'
cv.NamedWindow(backgroundWindow, cv.CV_WINDOW_AUTOSIZE)

sourceWindow = 'Source'
cv.NamedWindow(sourceWindow, cv.CV_WINDOW_AUTOSIZE)

subWindow = 'Sub'
cv.NamedWindow(subWindow, cv.CV_WINDOW_AUTOSIZE)

# Store center point of object
oldCenterPoint = (0,0)
background = None
while(True):
    # Get next frame
    sourceFrame = cv.QueryFrame(capture)
    if(sourceFrame == None):
        break
    
    # Set first background
    if(background == None):
        
        background = cv.CreateImage((sourceFrame.width, sourceFrame.height), sourceFrame.depth, sourceFrame.nChannels)
        
        # Horizontal flipping of the image
        cv.Flip(sourceFrame, background, HORIZONTAL_FLIP)
        cv.Smooth(background, background, cv.CV_GAUSSIAN)
        
    
    frame = cv.CreateImage((sourceFrame.width, sourceFrame.height), sourceFrame.depth, sourceFrame.nChannels)
    # Horizontal flipping of the image
    cv.Flip(sourceFrame, frame, HORIZONTAL_FLIP)
    
    cv.Smooth(frame, frame, cv.CV_GAUSSIAN)
    
    # Создает новое изображение, с такими же параметрами, как у всех изображений в видео 
    newBackground = cv.CreateImage((frame.width, frame.height), frame.depth, frame.nChannels)
    subCurrentFrame = cv.CreateImage((frame.width, frame.height), frame.depth, frame.nChannels)
    cv.Sub(frame, background, subCurrentFrame)
    cv.AddWeighted(background, alpha, frame, (1 - alpha), 0, newBackground)
    
    """
    # Show frame
    cv.ShowImage(sourceWindow, frame)
    cv.ShowImage(backgroundWindow, newBackground)
    """
    
    grayFrame = cv.CreateImage(cv.GetSize(frame), frame.depth, 1)
    cv.CvtColor(frame, grayFrame, cv.CV_RGB2GRAY)
    
    grayBack = cv.CreateImage(cv.GetSize(frame), frame.depth, 1)
    cv.CvtColor(background, grayBack, cv.CV_RGB2GRAY)

    cv.ShowImage(backgroundWindow, grayBack)
    
    print "debug"
    
    # Sub for gray images
    sub = cv.CreateImage(cv.GetSize(frame), frame.depth, 1)
    cv.AbsDiff(grayFrame, grayBack, sub)
    #cv.AbsDiffS(sub, sub, 0.5)
    
    """
    sub = cv.CreateImage(cv.GetSize(frame), frame.depth, frame.nChannels)
    cv.AbsDiff(frame, background, sub)
    cv.AbsDiffS(sub, sub, 100)
    """
    
    #medianBlur(foreground,foreground,9);
    cv.Smooth(sub, sub, cv.CV_GAUSSIAN, 3, 0)
    
    # threshold(foreground,foreground,128,255,THRESH_BINARY);
    #cv.AdaptiveThreshold(sub, sub, 255, cv.CV_ADAPTIVE_THRESH_GAUSSIAN_C, cv.CV_THRESH_BINARY, 9)
    cv.Threshold(sub, sub, 15, 255, cv.CV_THRESH_BINARY)
    
    #erode(foreground,foreground,Mat());
    cv.Erode(sub, sub, None, 10)
    #dilate(foreground,foreground,Mat());
    cv.Dilate(sub, sub, None, 18)
    
    cv.ShowImage(subWindow, sub)

    storage = cv.CreateMemStorage(0)
    contour = cv.FindContours(sub, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
    points = []

    while contour:
        bound_rect = cv.BoundingRect(list(contour))
        contour = contour.h_next()

        pt1 = (bound_rect[0], bound_rect[1])
        pt2 = (bound_rect[0] + bound_rect[2], bound_rect[1] + bound_rect[3])
        points.append(pt1)
        points.append(pt2)
        cv.Rectangle(frame, pt1, pt2, cv.CV_RGB(255,0,0), 1)

    if len(points):
        center_point = reduce(lambda a, b: ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), points)
        cv.Circle(frame, center_point, 40, cv.CV_RGB(255, 255, 255), 1)
        cv.Circle(frame, center_point, 30, cv.CV_RGB(255, 100, 0), 1)
        cv.Circle(frame, center_point, 20, cv.CV_RGB(255, 255, 255), 1)
        cv.Circle(frame, center_point, 10, cv.CV_RGB(255, 100, 0), 1)
        
        # draw line when object crossing screen center
        frameSize = cv.GetSize(frame)
        topPoint = (int(frameSize[0]/2), 0)
        bottomPoint = (int(frameSize[0]/2), frameSize[1])
        center = int(frameSize[0]/2)
        if(oldCenterPoint[0] < center and center < center_point[0]):
            cv.Line(frame, topPoint, bottomPoint, cv.Scalar(0,255,255), 5)
        elif(oldCenterPoint[0] > center and center > center_point[0]):
            cv.Line(frame, topPoint, bottomPoint, cv.Scalar(0,255,255), 5)
            
        # Save value of center point
        oldCenterPoint = center_point

    cv.ShowImage(sourceWindow, frame)
    

    # Обязательно нужна функция задержки!
    # Иначе видео пробегается моментально и на экране ничего не отображается!
    pressedKey = cv.WaitKey(33)
    # If user want to exit
    if(pressedKey == 27): # 27 - "Esc" code
        break
    
    background = newBackground
    
# Resources cleaning    
cv.DestroyAllWindows()