import cv2.cv as cv

def GetThresholdedImage(img):
    # Convert the image into an HSV image
    imgHSV = cv.CreateImage(cv.GetSize(img), 8, 3);
    cv.CvtColor(img, imgHSV, cv.CV_BGR2HSV);

    imgThreshed = cv.CreateImage(cv.GetSize(img), 8, 1);

    # Values 20,100,100 to 30,255,255 working perfect for blue at around 6pm
    cv.InRangeS(imgHSV, cv.Scalar(112, 100, 100), cv.Scalar(124, 255, 255), imgThreshed);

    return imgThreshed;

# Background stability  parameter
# 0 <= alpha <= 1
alpha = 0.99

capture = cv.CaptureFromCAM(0)   

# The two windows we'll be using
cv.NamedWindow("video");
cv.NamedWindow("thresh");

# This image holds the "scribble" data...
# the tracked positions of the ball
imgScribble = None;

posX = 0;
posY = 0;

while(True):

    # Will hold a frame captured from the camera
    frame = None;
    frame = cv.QueryFrame(capture);

    # If we couldn't grab a frame... quit
    if (frame == None):
        break

    # If this is the first frame, we need to initialize it
    if(imgScribble == None):
        imgScribble = cv.CreateImage(cv.GetSize(frame), 8, 3);

    # Holds the blue thresholded image (blue = white, rest = black)
    imgBlueThresh = GetThresholdedImage(frame);

    # Calculate the moments to estimate the position of the ball
    imgSeq = cv.GetMat(imgBlueThresh)
    moments = cv.Moments(imgSeq, 1);

    # The actual moment values
    moment10 = cv.GetSpatialMoment(moments, 1, 0);
    moment01 = cv.GetSpatialMoment(moments, 0, 1);
    area = cv.GetCentralMoment(moments, 0, 0);

    print moment10
    print moment01
    print area

    # Holding the last and current ball positions
    lastX = posX;
    lastY = posY;

    if(area != 0):
        posX = moment10 / area;
        posY = moment01 / area;

    # Print it out for debugging purposes
    print 'position (%d, %d) \n' % (posX, posY);

    # We want to draw a line only if its a valid position
    if (lastX > 0 and lastY > 0 and posX > 0 and posY > 0):
        # Draw a blue line from the previous point to the current point
        cv.Line(imgScribble, (int(posX), int(posY)), (int(lastX), int(lastY)), cv.Scalar(0,255,255), 5);

    # Add the scribbling image and the frame... and we get a combination of the two
    cv.Add(frame, imgScribble, frame);
    cv.ShowImage("thresh", imgBlueThresh);
    cv.ShowImage("video", frame);

    # Wait for a keypress
    pressedKey = cv.WaitKey(33)
    # If user want to exit
    if(pressedKey == 27): # 27 - "Esc" code
        break

# Resources cleaning    
cv.DestroyAllWindows()




