# Программа выводит последовательность кадров видео из avi файла
# Usage : python display.py <video_file>
# video_file - путь до файла в формате avi

import sys
import cv2.cv as cv

if(len(sys.argv) != 2):
    print "Usage : python display.py <video_file>"

else:
    filename = sys.argv[1];
    capture = cv.CreateFileCapture(filename)
    
    mainWindow = 'Main'
    cv.NamedWindow(mainWindow, cv.CV_WINDOW_AUTOSIZE)
    
    frame = None
    while(True):
        # Get next frame
        frame = cv.QueryFrame(capture)
        if(frame == None):
            break
        
        # Show frame
        cv.ShowImage(mainWindow, frame)

        # Обязательно нужна функция задержки!
        # Иначе видео пробегается моментально и на экране ничего не отображается!
        pressedKey = cv.WaitKey(33)
        # If user want to exit
        if(pressedKey == 27): # 27 - "Esc" code
            break
        
    # Resources cleaning    
    cv.DestroyAllWindows()