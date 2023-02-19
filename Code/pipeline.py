import os
import cv2
import numpy as np
import time
from frameDiff import FrameDiff
from faceDetect import FaceDetect
from faceRecog import FaceRecog
from antiSpoof import Antispoof
from input import clickInput

class Pipeline:
    def __init__():
        clickInput()

        antiSpoof = Antispoof()
        diff = FrameDiff(0.92)
        detect = FaceDetect(0.50,"cpu")
        rec = FaceRecog(threshold = 0.3, metric = "cosine")

    def runPipeline(video=0,source = "../Data/user.png"):
        cap = cv2.VideoCapture(video)
        user = cv2.resize(cv2.imread(source),(1000,1000))
        ret, curr_frame = cap.read()
        prev_frame = cv2.resize(curr_frame,(600, 400))
        print("read first frame")
        ret, curr_frame = cap.read()
        curr_frame = cv2.resize(curr_frame,(600, 400))
        frameCount = 2
        frameSkip = 10
        noFaceCount = 0
        multipleFaceCount = 0
        unverifiedFaceCount = 0
        spoofedFaceCount=0
        outputStr = "{}, {}, {}\n"
        file = open("pipeline_output.txt","w")
        start_time =time.time()
        while True:
            try:
                frame_input_time = time.time()
                diff_val, diff_score = diff.ssim(prev_frame, curr_frame)
                if diff_val:
                    cv2.putText(curr_frame, 'Frame Change', (0,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                    print("diff frame", diff_score)
                    numFaces, conf ,boxes = detect.detect(curr_frame)

                    if numFaces==1:
                        print("1 face detected")
                        (x,y,w,h) = boxes[0]
                        x, y, w, h = int(x), int(y), int(w), int(h)
                        text = f"{conf[0]*100:.2f}%"
                        cv2.putText(curr_frame,text,(x, y - 20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0, 255, 0),1)
                        cv2.rectangle(curr_frame, (x, y), (w, h), (0, 255, 0), 1)
                        isSame, distance = rec.verify(curr_frame,user)
                        if(isSame):
                            cv2.putText(curr_frame, 'Face Verified', (0,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                            print("face is verified", distance)
                            #antispoof
                            spoof_result = antiSpoof.predict_spoof(curr_frame)
                            if spoof_result[0]==2:
                                print("face is Fake", spoof_result[1])
                                cv2.putText(curr_frame, 'Spoofed Face Detected', (0,45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                                file.write(outputStr.format("Spoofed Face Detected",frameCount,time.time()-start_time))
                                spoofedFaceCount+=1

                        else:
                            cv2.putText(curr_frame, 'Face Not Verified', (0,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                            print("face is not verified", distance)
                            file.write(outputStr.format("Face Not Verified",frameCount,time.time()-start_time))
                            unverifiedFaceCount+=1

                        
                    elif numFaces==0:
                        print("0 face detected")
                        cv2.putText(curr_frame, 'No Faces', (0,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                        file.write(outputStr.format("No Faces Detected",frameCount,time.time()-start_time))
                        noFaceCount+=1
                    else:
                        print("multiple faces detected")
                        cv2.putText(curr_frame, 'Multiple Faces', (0,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                        file.write(outputStr.format("Multiple Faces Detected",frameCount,time.time()-start_time))
                        multipleFaceCount+=1
                cv2.imshow('frame',curr_frame)
                processing_time = time.time()
                time_diff = processing_time - frame_input_time
                time_total = processing_time -start_time
                frameCount+=frameSkip
                cap.set(cv2.CAP_PROP_POS_FRAMES,frameCount)
                prev_frame = curr_frame.copy()
                ret, curr_frame = cap.read()
                curr_frame = cv2.resize(curr_frame,(600,400))
            except cv2.error:
                break
            if cv2.waitKey(25) & 0xFF == ord("q"):
                break
        file.write("Summary\n")
        file.write("1. Missing Face: "+str(noFaceCount)+"\n")
        file.write("2. Multiple Faces in Frame: "+str(multipleFaceCount)+"\n")
        file.write("3. Unverified User: "+ str(unverifiedFaceCount)+"\n")
        file.write("4. Spoofed Face Count: "+ str(spoofedFaceCount)+"\n")
        file.close()
        cap.release()
        cv2.destroyAllWindows()
        
    runPipeline()

