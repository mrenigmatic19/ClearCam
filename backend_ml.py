import cv2
import numpy as np
import os
import multiprocessing as mp

def darkChannel(img,r = 7):
    return cv2.erode(np.min(img,2),np.ones((2 * r + 1, 2 * r + 1)))
    


def estimateA(img,darkChann):
    imgCopy = img.copy() 
    h,w,_  = img.shape
    length = h*w
    num    = max(int(length *0.0001),1)
    DarkChannVec = np.reshape(darkChann,length) 
    index  = DarkChannVec.argsort()[length-num:]
    rowIdx = index // w
    colIdx = index %  w
    coords = np.stack((colIdx,rowIdx),axis = 1)
    sumA   = np.zeros((1,3))
    for coord in coords:
        col,row = coord
        sumA    += img[row,col,:]
    A = sumA / num
    return A 


def estimateT(img,A,omega = 0.95):
    tempMap = np.empty(img.shape,img.dtype)
    tempMap = img / A
    transmissionMap = 1 - omega * darkChannel(tempMap)
    return transmissionMap

def guidedfilter(I, p, r, eps = 0.0001):
    height, width = I.shape
    m_I = cv2.boxFilter(I, -1, (r, r))
    m_p = cv2.boxFilter(p, -1, (r, r))
    m_Ip = cv2.boxFilter(I * p, -1, (r, r))
    cov_Ip = m_Ip - m_I * m_p

    m_II = cv2.boxFilter(I * I, -1, (r, r))
    var_I = m_II - m_I * m_I

    a = cov_Ip / (var_I + eps)
    b = m_p - a * m_I

    m_a = cv2.boxFilter(a, -1, (r, r))
    m_b = cv2.boxFilter(b, -1, (r, r))
    return m_a * I + m_b


def deHaze(adress,r = 7,T_threshold = 0.1):
    img = cv2.imread('%s'%adress)
    imgNormal = img / 255
    darkChann  = darkChannel(imgNormal,r)
    A = estimateA(imgNormal,darkChann)
    T = estimateT(imgNormal,A)
    imgGray    = np.min(img,2) / 255
    T_refine   = guidedfilter(imgGray,T,81)
    imgRecover = np.empty(imgNormal.shape,imgNormal.dtype)
    T = cv2.max(T_refine,T_threshold)
    for i in range(3):
        imgRecover[:,:,i] = (imgNormal[:,:,i] - A[0,i]) / T + A[0,i] 
   
    imgRecover=imgRecover*255
    cv2.imwrite("%s"%adress,imgRecover)
    


if __name__ == '__main__':
    vidcap = cv2.VideoCapture("C:\\Users\\Asus\\Documents\\GitHub\\imagedehaze\\uploads\\input.mp4")

    success, image = vidcap.read()
    count = 1

    print(success)
    while success:
        cv2.imwrite("video_data/%09d.jpg" % count, image)    
        success, image = vidcap.read()
        count += 1
    vidcap.release() 
    
    path = './video_data/'
    out_path = './uploads/'

    pre_imgs = os.listdir(path)   
    image=[]
    processes=[]
    count=1
    for i in pre_imgs:
        i = path+i
        if(count%8!=0):
            p=mp.Process(target=deHaze,args=[i])
            processes.append(p)
        else:
            processes.append(i)
        count=count+1
        
    count=1
    for i in processes:
        if(count%8!=0):
            i.start()
        else:
            deHaze(i)
        count=count+1

    out_video_full_path = out_path+'output.mp4'

    pre_imgs = os.listdir(path)

    print(pre_imgs)
    img = []

    for i in pre_imgs:
        i = path+i
        print(i)
        img.append(i)



    cv2_fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    frame = cv2.imread(img[0])
    size = list(frame.shape)
    del size[2]
    size.reverse()

    video = cv2.VideoWriter(out_video_full_path, cv2_fourcc, 30, size)

    for i in range(len(img)): 
        video.write(cv2.imread(img[i]))
        

    video.release()
    cv2.destroyAllWindows()

        
        