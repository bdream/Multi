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
alpha = 0.9

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
    cv.AddWeighted(background, alpha, frame, (1 - alpha), 0, newBackground)
    
    # Show frame
    cv.ShowImage(sourceWindow, frame)
    cv.ShowImage(backgroundWindow, newBackground)
    
    grayFrame = cv.CreateImage(cv.GetSize(frame), frame.depth, 1)
    cv.CvtColor(frame, grayFrame, cv.CV_RGB2GRAY)
    
    grayBack = cv.CreateImage(cv.GetSize(frame), frame.depth, 1)
    cv.CvtColor(newBackground, grayBack, cv.CV_RGB2GRAY)
    
    print "debug"
    
    sub = cv.CreateImage(cv.GetSize(frame), frame.depth, 1)
    cv.AbsDiff(grayFrame, grayBack, sub)
    
    cv.ShowImage(subWindow, sub)
    
    """
    sub = cv.CreateImage(cv.GetSize(frame), frame.depth, frame.nChannels)
    cv.AbsDiff(frame, background, sub)
    """
    
    # threshold(foreground,foreground,128,255,THRESH_BINARY);
    cv.Threshold(sub, sub, 128, 255, cv.CV_THRESH_BINARY)
    
    #medianBlur(foreground,foreground,9);
    cv.Smooth(sub, sub, cv.CV_BLUR)
    #erode(foreground,foreground,Mat());
    cv.Erode(sub, sub)
    #dilate(foreground,foreground,Mat());
    cv.Dilate(sub, sub)

    #cv.ShowImage(subWindow, sub)

    # Обязательно нужна функция задержки!
    # Иначе видео пробегается моментально и на экране ничего не отображается!
    pressedKey = cv.WaitKey(33)
    # If user want to exit
    if(pressedKey == 27): # 27 - "Esc" code
        break
    
    background = newBackground
    
# Resources cleaning    
cv.DestroyAllWindows()