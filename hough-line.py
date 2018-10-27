#edit by yuzhe
#2018/10/27

import cv2
from imutils.video import FPS#计算fps库
import numpy as np

# capture = cv2.VideoCapture("1.mov")#视频流
# capture = cv2.VideoCapture("rtsp://admin:12345@192.168.1.185:554//Streaming/Channels/1")#网络摄像机
capture = cv2.VideoCapture(0)#本地摄像头
if capture.isOpened():
    fps = FPS().start()
    while True:
        ret, prev = capture.read()
        if ret == True:
            try:

                img = cv2.resize(prev, (320, 240))
                img = cv2.GaussianBlur(img, (3, 3), 0)
                edges = cv2.Canny(img, 50, 150, apertureSize=3)
                lines = cv2.HoughLines(edges, 1, np.pi / 180, 118)
                result = img.copy()
                for line in lines[0]:
                    rho = line[0]
                    theta = line[1]

                    if (theta < (np.pi / 4.)) or (theta > (3. * np.pi / 4.0)):

                        pt1 = (int(rho / np.cos(theta)), 0)

                        pt2 = (int((rho - result.shape[0] * np.sin(theta)) / np.cos(theta)), result.shape[0])

                        cv2.line(result, pt1, pt2, (255))
                    else:

                        pt1 = (0, int(rho / np.sin(theta)))

                        pt2 = (result.shape[1], int((rho - result.shape[1] * np.cos(theta)) / np.sin(theta)))

                        cv2.line(result, pt1, pt2, (255), 1)
                        print(pt1[0], pt1[1], pt2[0], pt2[1])
                        cv2.circle(result, (pt1[0], pt1[1]), 10, (0, 0, 255), -1)
                        cv2.circle(result, (pt2[0], pt2[1]), 10, (0, 0, 255), -1)
                        cv2.circle(result, (int((pt1[0] + pt2[0]) / 2), int((pt1[1] + pt2[1]) / 2)), 10, (0, 0, 255),
                                   -1)

            except TypeError:
                print('error')
                pass
            cv2.imshow('Result', result)


        else:
            break
        if cv2.waitKey(1) == 50:
            break
        fps.update()
        fps.stop()
        print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

capture.release()
cv2.destroyAllWindows()