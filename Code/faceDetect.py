import cv2
from facenet_pytorch import MTCNN
import torch

class FaceDetect:
    def __init__(self,confidence_threshold,device):
        self.confidence_threshold = confidence_threshold
        self.mtcnn = MTCNN(keep_all=True, device=device)
    def detect(self,frame):
        boxes = []
        conf = []
        boxes, conf = self.mtcnn.detect(frame)
        numFaces = 0
        if conf[0]!=None:
            for i in conf:
                if i > self.confidence_threshold:
                    numFaces+=1
        return (numFaces, conf ,boxes)


# fd = FaceDetect(0.50,"cpu")
# img1 = cv2.imread("/home/siddharth/Downloads/images.jpeg")
# img2 = cv2.imread("/home/siddharth/Downloads/face.jpeg")
# print("1\n",fd.detect(img1))
# print("2\n",fd.detect(img2))          