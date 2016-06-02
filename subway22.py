#-*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import urllib.request
import datetime, time
import subwaybook
from datetime import timedelta
loopFlag = 1

today = str(datetime.date.today() + timedelta(days = -10))
url = 'http://openapi.seoul.go.kr:8088/4d756363586e793331303646594b6b4c/xml/CardSubwayStatsNew/1/549/'+today.replace('-','')


tree = ET.ElementTree(file=urllib.request.urlopen(url))
root = tree.getroot()


def Search(sub) :
    subName = sub.split(' ')[0]

    
    for data in root.iter("row") :
        #if data.findtext("LINE_NUM").find(LINE_NUM) != -1 :
        if data.findtext("SUB_STA_NM").find(subName) != -1 :
            string = "라인 : {0}\n승차 : {1}\n하차 : {2}".format(data.findtext("LINE_NUM"),data.findtext("RIDE_PASGR_NUM"), data.findtext("ALIGHT_PASGR_NUM"))
            return string

        

def Allprint():
    for a in root.findall("row"):
        print(a.findtext('USE_DT'))
        print(a.findtext('LINE_NUM'))
        print(a.findtext('SUB_STA_NM'))
        print(a.findtext('RIDE_PASGR_NUM'))
        print(a.findtext('ALIGHT_PASGR_NUM'))
        print('----------------------')
     

def launcherFunction(menu):
    if menu == 'p':
        Allprint()
    elif menu == 's':
        keyword = input ('역을 입력해 주세요 :')
        print(Search(keyword))
        print('----------------------')
    elif menu == 'm':
        subwaybook.sendMain()
    elif menu=='q':
        global loopFlag
        print("종료합니다.")
        loopFlag = -1

while(loopFlag>0):
    #if __name__ == "__main__" :
        print("전체출력 : p")
        print("검색 : s")
        print("이메일 전송: m")
        print("종료 : q")
        menuKey = str(input ('input menu:'))
        launcherFunction(menuKey)

def main():
    launcherFunction()
