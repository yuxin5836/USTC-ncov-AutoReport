import time
import datetime
import pytz
import re
import sys
import argparse
from bs4 import BeautifulSoup
import requests
import json
from io import BytesIO
import pytesseract
from PIL import Image, ImageDraw
import numpy as np
import cv2

class Login:
    def __init__(self, stuid, password, origin, service, exam, session=None):
        self.stuid=stuid
        self.password=password
        self.origin=origin
        self.service=service
        self.exam=exam
        if session==None:
            self.session=requests.Session()
        else:
            self.session=session
        
    def get_LT(self,JSESSIONID):
        headers={
            'Accept': 'image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'Cookie': 'JSESSIONID='+JSESSIONID+'; lang=zh',
            'Host': 'passport.ustc.edu.cn',
            'Referer': 'https://passport.ustc.edu.cn/login?service='+self.service,
            'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Microsoft Edge";v="92"',
            'sec-ch-ua-mobile': '?0',
            'Sec-Fetch-Dest': 'image',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.78'
        } 
        text=self.session.get('https://passport.ustc.edu.cn/validatecode.jsp?type=login',headers=headers,stream=True).content
        image=Image.open(BytesIO(text))
        image=cv2.cvtColor(np.asarray(image),cv2.COLOR_RGB2BGR)
        kernel = np.ones((3,3),np.uint8)
        image = cv2.dilate(image,kernel,iterations = 1)
        image = cv2.erode(image,kernel,iterations = 1)
        Image.fromarray(image).show()
        return pytesseract.image_to_string(Image.fromarray(image))[:4]
    def passport(self):
        data=self.session.get('https://passport.ustc.edu.cn/login?service='+self.service)
        JSESSIONID=data.cookies.get('JSESSIONID')
        data=data.text
        data = data.encode('ascii','ignore').decode('utf-8','ignore')
        soup = BeautifulSoup(data, 'html.parser')
        CAS_LT = soup.find("input", {"name": "CAS_LT"})['value']
        LT=self.get_LT(JSESSIONID)
        data = {
            'model': 'uplogin.jsp',
            'service': self.service,
            'warn': '',
            'showCode': '1',
            'username': self.stuid,
            'password': str(self.password),
            'button': '',
            'CAS-LT':CAS_LT,
            'LT':LT
        }
        print(data)
        self.session.post('https://passport.ustc.edu.cn/login', data=data)
    def login(self):
        loginsuccess = False
        retrycount = 5
        while (not loginsuccess) and retrycount:
            self.passport()
            cookies = self.session.cookies
            self.result = self.session.get(self.origin)
            retrycount = retrycount - 1
            if self.result.url != self.exam:
                print("Login Failed! Retry...")
            else:
                print("Login Successful!")
                loginsuccess = True
        if not loginsuccess:
            return False
rpt=Login('PB20000000','******','https://weixine.ustc.edu.cn/2020','https://weixine.ustc.edu.cn/2020/caslogin','https://weixine.ustc.edu.cn/2020/home')
rpt.login()
