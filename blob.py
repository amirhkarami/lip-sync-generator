import  cv2 as cv
import numpy as np
import pandas as pd 

haar_cascade_eyes = cv.CascadeClassifier('eye detector\haarcascade_eye_tree_eyeglasses.xml')
sort_check=['E_LUL','E_LUM','E_LUR','E_LDL','E_LDM','E_LDR','E_M','E_RUL','E_RUM','E_RUR','E_RDL','E_RDM','E_RDR']

def eye_detection(frame,dataset):
    eyes_rect=haar_cascade_eyes.detectMultiScale(frame,scaleFactor=4,minNeighbors=1)
    if len(eyes_rect)==2:
        return left_eye_right_eye(eyes_rect)
    else:
        return



def left_eye_right_eye(eyes):
    if eyes[0][0]>eyes[1][1]:
        return eyes
    else:
        return([eyes[1],eyes[0]])




def blobs_tuple_to_list(blobs):
    if type(blobs)==list:
        return blobs
    lst=[]
    for i in range(len(blobs)):
        for j in range(2):
            lst.append(blobs[i].pt[j])
    return lst





def blob_y_sort(lst):
    lst=blobs_tuple_to_list(lst)
    n = len(lst)
    for i in range(n):
        for j in range(1, n-4,2):
            if lst[j] > lst[j+2] :
                lst[j-1] , lst[j],lst[j+1],lst[j+2]= lst[j+1],lst[j+2],lst[j-1] , lst[j]  




    return lst
def blob_x_sort(lst):
    lst=blobs_tuple_to_list(lst)
    n = len(lst)
    for i in range(n):
        for j in range(0, n-4,2):
            if lst[j] > lst[j+2] :
                lst[j] , lst[j+1],lst[j+2],lst[j+3]= lst[j+2],lst[j+3],lst[j] , lst[j+1]  
  
    return lst




def eyes_x_sort(lst): 
    n = len(lst) 
    for i in range(n): 
        for j in range(0, n-4,2):
            if lst[j] > lst[j+2] :
                lst[j] , lst[j+1],lst[j+2],lst[j+3]= lst[j+2],lst[j+3],lst[j] , lst[j+1]  

    return lst




def forehead(lst):
    result=blob_x_sort(lst)[:6]
    maxx=0
    for i in range(3):
        for j in range(0,6-2,2):
            if result[j]>result[j+2]:
                result[j],result[j+1],result[j+2],result[j+3]=result[j+2],result[j+3], result[j],result[j+1]
    return result


def eye_x_sorter(lst):
    result=lst
    maxx=0
    for i in range(3):
        for j in range(0,6-2,2):
            if result[j]>result[j+2]:
                result[j],result[j+1],result[j+2],result[j+3]=result[j+2],result[j+3], result[j],result[j+1]
    return result



def eyes_blob(lst):
    lst=eyes_x_sort(blob_y_sort(lst)[6:32])
    left_eye=lst[:12]
    between_eyes=[12,13]
    right_eye=lst[14:]
    #print(lst)
    return lst
camera=cv.VideoCapture(0)

def eyes_blob_y_sort(lst):
    for i in range(6):
        for j in range(1,12,2):
            if lst[j]>lst[j+2]:
                lst[j-1],lst[j],lst[j+1],lst[j+2]=lst[j+1],lst[j+2],lst[j-1],lst[j]
    lower=lst[:6]
    upper=lst[6:12]
def eyes_draw(blobs,frame):
    #print(blobs)
    blobs=blob_y_sort(blobs)
    
    upper=eye_x_sorter(blobs)[:6]
    lower=eye_x_sorter(blobs)[6:]
    #print(upper,lower)
    #upper=blob_x_sort(upper)
    lower=blob_x_sort(lower)
    cv.line(num,(round(upper[0]),round(upper[1])),(round(upper[2]),round(upper[3])),(0,255,0),1)
    cv.line(num,(round(upper[2]),round(upper[3])),(round(upper[4]),round(upper[5])),(0,0,255),1)
    cv.line(num,(round(upper[0]),round(upper[1])),(round(lower[0]),round(lower[1])),(255,0,0),1)
    cv.line(num,(round(lower[0]),round(lower[1])),(round(lower[2]),round(lower[3])),(255,50,0),1)
    cv.line(num,(round(lower[2]),round(lower[3])),(round(lower[0]),round(lower[1])),(255,0,0),1)
    cv.line(num,(round(upper[4]),round(upper[5])),(round(lower[4]),round(lower[5])),(255,0,0),1)
    cv.line(num,(round(lower[2]),round(lower[3])),(round(lower[4]),round(lower[5])),(0,0,255),1)
    return

def lips_blobs(blobs,frame):
    lower=blobs[6:]
    upper=blobs[:6]
    upper=eye_x_sorter(lower)
    lower=eye_x_sorter(upper)
    cv.line(num,(round(upper[0]),round(upper[1])),(round(upper[2]),round(upper[3])),(0,255,0),1)
    cv.line(num,(round(upper[2]),round(upper[3])),(round(upper[4]),round(upper[5])),(0,0,255),1)
    cv.line(num,(round(upper[0]),round(upper[1])),(round(lower[0]),round(lower[1])),(255,0,0),1)
    cv.line(num,(round(lower[0]),round(lower[1])),(round(lower[2]),round(lower[3])),(255,50,0),1)
    cv.line(num,(round(lower[2]),round(lower[3])),(round(lower[0]),round(lower[1])),(255,0,0),1)
    cv.line(num,(round(upper[4]),round(upper[5])),(round(lower[4]),round(lower[5])),(255,0,0),1)
    cv.line(num,(round(lower[2]),round(lower[3])),(round(lower[4]),round(lower[5])),(0,0,255),1)   
    return
detector = cv.SimpleBlobDetector_create()
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('output.avi', fourcc, 30.0, (1280,720),False)
while True:
    num=np.zeros((1280,720))
    check,frame=camera.read()
    blobs = detector.detect(frame)
    blobs1=blobs_tuple_to_list(blobs)
    if len(blobs)>2:
        forehead_lines=forehead(blob_y_sort(blobs)[0:6])
        right_cheek=blob_x_sort(blobs)[0:2]
        eyes=blob_y_sort(blobs)[6:32]
        eyes=blob_x_sort(eyes)
        print(len(eyes))
        left_eye=eyes[:12]
        middle_eye=eyes[12:14]
        right_eye=eyes[14:]
        if len(eyes)==26:
            eyes_draw(left_eye,frame)
            eyes_draw(right_eye,frame)
            lips=blob_y_sort(blobs)[-12:]
            lips_blobs(lips,frame)
        cv.line(num,(round(forehead_lines[0]),round(forehead_lines[1])),(round(forehead_lines[2]),round(forehead_lines[3])),(255,0,0),1)
        cv.line(num,(round(forehead_lines[2]),round(forehead_lines[3])),(round(forehead_lines[4]),round(forehead_lines[5])),(255,0,0),1)
        cv.line(num,(round(right_cheek[0]),round(right_cheek[1])),(round(forehead_lines[0]),round(forehead_lines[1])),(255,0,0),1)
        cv.imshow('forehead',frame)
    else:
        key=cv.waitKey(1)
        if key==ord('q'):
            camera.release()
            cv.destroyAllWindows()
            break
            
       
    blobs_drawer = cv.drawKeypoints(frame, blobs, num, (0,0,255), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    out.write(num)
    cv.imshow('n',frame)
    cv.imshow('b',num)


    
  
    
    key=cv.waitKey(1)
    if key==ord('q'):
        camera.release()
        cv.destroyAllWindows()
        out.release()
        break

