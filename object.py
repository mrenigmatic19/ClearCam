import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
vidcap = cv2.VideoCapture("D:\\GitHub\\ClearCam\\uploads\\input.mp4")
success=True
count=0
while success:

    success,frame=vidcap.read()
    count=count+1
    if count%6==0:
        continue
    bbox,label,conf=cv.detect_common_objects(frame)
    frame=draw_bbox(frame,bbox,label,conf)
    c=label.count('car')
    cv2.putText(frame,str(c),(50,60),cv2.FONT_HERSHEY_SIMPLEX,3,(255,255,255),3)
    p=label.count('truck')
    cv2.putText(frame,str(p),(50,160),cv2.FONT_HERSHEY_SIMPLEX,3,(255,255,255),3)
    cv2.imshow("FRAME",frame)
    if cv2.waitKey(1)&0xFF==27:
        break
frame.release()
cv2.destroyAllWindows()