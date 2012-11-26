# Программа неподвижный фон видео, убирая движущиеся объекты

import sys
import cv2.cv as cv

# Параметр, устойчивости фона
# 0 <= alpha <= 1
# Чем меньше, тем фон менее устойчив 
alpha = 0.99

if(len(sys.argv) != 2):
    print "Usage : python display.py <video_file>"

else:
    filename = sys.argv[1];
    capture = cv.CreateFileCapture(filename)
    
    if(capture is None):
        print "Error: file can't be open"
        exit()
        
    backgroundWindow = 'Background'
    cv.NamedWindow(backgroundWindow, cv.CV_WINDOW_AUTOSIZE)
    
    sourceWindow = 'Source'
    cv.NamedWindow(sourceWindow, cv.CV_WINDOW_AUTOSIZE)
    
    subWindow = 'Sub'
    cv.NamedWindow(subWindow, cv.CV_WINDOW_AUTOSIZE)    
    
    background = cv.QueryFrame(capture)
    frame = None
    while(True):
        # Get next frame
        frame = cv.QueryFrame(capture)
        if(frame == None):
            break
        
        # Создает новое изображение, с такими же параметрами, как у всех изображений в видео 
        newBackground = cv.CreateImage((frame.width, frame.height), frame.depth, frame.nChannels)
        cv.AddWeighted(background, alpha, frame, (1 - alpha), 0, newBackground)
        
        # Show frame
        cv.ShowImage(sourceWindow, frame)
        cv.ShowImage(backgroundWindow, newBackground)
        
        sub = cv.CreateImage((frame.width, frame.height), frame.depth, frame.nChannels)
        cv.Sub(background, frame, sub)
        cv.ShowImage(subWindow, sub)

        # Обязательно нужна функция задержки!
        # Иначе видео пробегается моментально и на экране ничего не отображается!
        pressedKey = cv.WaitKey(33)
        # If user want to exit
        if(pressedKey == 27): # 27 - "Esc" code
            break
        
        background = newBackground
    # Resources cleaning    
    cv.DestroyAllWindows()


