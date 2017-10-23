# _*_ coding:utf-8 _*_
import os
import sys
from PIL import Image, ImageDraw
import numpy as np
import cv2


def detect_object(infile):
    image = cv2.imread(infile)
    size = image.shape[:2] # 获得当前桢彩色图像的大小
    # image_set=np.zeros(size,dtype=np.float16)#定义一个与当前桢图像大小相同的的灰度图像矩阵
    # image_grey = Image.new(mode= “RGBA”,size = size, color = (117,255,0))
    #image_grey = cv2.imread(img_grey)
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 将当前桢图像转换成灰度图像
    # img_binary = cv2.threshold(image,127,255,0)#将灰度图片转化为二进制图片
    color = (220,20,60)  # 设置人脸框的颜色
    # eye_cascade = cv2.CascadeClassifier(‘/Users/liuqi/opencv/data/haarcascades/haarcascade_eye.xml’)
    classfier = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
    # 人脸检测，1.2和2分别为图片缩放比例和需要检测的有效点数
    faceRects = classfier.detectMultiScale(
        grey, scaleFactor=1.3, minNeighbors=1, minSize=(32, 32))
    result = []
    im = Image.open(infile)
    # 大于0则检测到人脸
    if len(faceRects) > 0:
        draw = ImageDraw.Draw(im)
        num = 0
        for faceRect in faceRects:
            x, y, w, h = faceRect
            cv2.rectangle(image, (x, y), (x+w, y+h), color,5)
            # 将当前帧保存为图片 
            # cv2.imwrite(file_name,image_grey)
            num  = num+1
        namenum = bytes(num)
        cv2.imwrite("113"+namenum+".jpg", image)
    else:
        print("Error: cannot detect faces on % s" % infile)
        return 0


def process(infile):
    faces = detect_object(infile)

if __name__ == "__main__":
    process("13.jpg")
