# -*- coding: UTF-8 -*-
import os
import sys
import time
from cv2 import cv2 as cv

# 截图数量
screenImgNum = 0
# 消息所处坐标
addMsgPos = []
# send所处坐标
sendMsgPos = []


# 获取文件截图
def getScreen(fileName):
    screenInfo = "/sdcard/{}.png".format(fileName)
    fileSavePath = ".\\lib\\{}.png".format(fileName)
    screenCmd = "{} {} {}".format(execPath, screenPath, screenInfo)
    pullCmd = "{} pull {} {}".format(execPath, screenInfo, fileSavePath)
    global screenImgNum
    screenImgNum += 1
    os.system(screenCmd)
    os.system(pullCmd)
    showScreenImg(fileName)


# 添加消息到输入框
def touchHandler(row, col):
    addCmd = "{} {} {}".format(tapCmd, row, col)
    print(addCmd)
    os.system(addCmd)
    # 加载一张图片以后，继续添加
    if screenImgNum == 1:
        getScreen('sendScreen')


# 保存截图点击坐标
def saveTapPos(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        # 当图片数量大于点击次数
        if screenImgNum > touchTimes:
            global sendMsgPos
            sendMsgPos = [x*resize, y*resize]
        else:
            global addMsgPos
            addMsgPos.append([x*resize, y*resize])
        cv.circle(param, (x, y), 10, (132, 112, 255), -1)


# 展示截图选择数据
def showScreenImg(fileName):
    imagePath = "./lib/{}.png".format(fileName)
    img = cv.imread(imagePath)
    height, width, _ = img.shape
    resizedImg = cv.resize(img, (width//resize, height//resize))
    cv.namedWindow('screen')
    cv.setMouseCallback('screen', saveTapPos, resizedImg)
    while 1:
        cv.imshow("screen", resizedImg)
        k = cv.waitKey(1)
        if k == 27:
            cv.destroyWindow('screen')
            break
    if screenImgNum > touchTimes:
        start()
    elif screenImgNum == 1:
        time.sleep(1)
        touchHandler(addMsgPos[0][0], addMsgPos[0][1])
    else:
        getScreen("msgScreen{}".format(screenImgNum))


# 循环执行信息发送
def start():
    for num in range(0, times):
        print("第{}次执行".format(num+1))
        time.sleep(sleepTime)
        if num != 0:
            index = num % touchTimes
            touchHandler(addMsgPos[index][0], addMsgPos[index][1])
        touchHandler(sendMsgPos[0], sendMsgPos[1])


if __name__ == '__main__':
    # adb执行位置
    execPath = ".\\lib\\adb.exe"
    # 点击命令
    tapCmd = "{} shell input tap".format(execPath)
    # 截图命令
    screenPath = "shell /system/bin/screencap -p"
    # 执行间隔时间(单位:秒)
    sleepTime = 0.3
    # 执行次数
    times = int(input("请输入执行次数："))
    # 设置截图缩放比例
    resize = int(input("请输入图片展示缩放倍数："))
    # 选择点击次数
    touchTimes = int(input("请输入点击表情次数："))

    getScreen('msgScreen')
