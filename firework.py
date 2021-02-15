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
    fileSavePath = "{}\\img\\{}.png".format(sys.path[0], fileName)
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
        if screenImgNum == 1:
            global addMsgPos
            addMsgPos = [x*2, y*2]
            print('addMsgPos', addMsgPos)
        elif screenImgNum > 1:
            global sendMsgPos
            sendMsgPos = [x*2, y*2]
            print('sendMsgPos', sendMsgPos)
        cv.circle(param, (x, y), 10, (22, 255, 0), -1)


# 展示截图选择数据
def showScreenImg(fileName):
    imagePath = os.path.join("img/{}.png".format(fileName))
    img = cv.imread(imagePath)
    height, width, _ = img.shape
    resizedImg = cv.resize(img, (width//2, height//2))
    cv.namedWindow('screen')
    cv.setMouseCallback('screen', saveTapPos, resizedImg)
    while 1:
        cv.imshow("screen", resizedImg)
        k = cv.waitKey(1)
        if k == 27:
            break
    if screenImgNum == 1:
        time.sleep(3)
        touchHandler(addMsgPos[0], addMsgPos[1])
    elif screenImgNum > 1:
        start()


def start():
    for num in range(0, times):
        print(num)
        time.sleep(sleepTime)
        if num != 0:
            touchHandler(addMsgPos[0], addMsgPos[1])
        touchHandler(sendMsgPos[0], sendMsgPos[1])


if __name__ == '__main__':
    # adb执行位置
    execPath = ".\\lib\\adb.exe"
    # 点击命令
    tapCmd = "{} shell input tap".format(execPath)
    # 截图命令
    screenPath = "shell /system/bin/screencap -p"
    # 执行次数
    times = 99
    # 执行间隔时间(单位:秒)
    sleepTime = 0.3

    getScreen('msgScreen')
