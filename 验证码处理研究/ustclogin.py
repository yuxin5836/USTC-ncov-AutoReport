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
    def __init__(self, stuid, password, origin, service, exam):
        self.stuid=stuid
        self.password=password
        self.origin=origin
        self.service=service
        self.exam=exam
        
    def get_LT(self,JSESSIONID):
        text=self.session.get('https://passport.ustc.edu.cn/validatecode.jsp?type=login',stream=True).content
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
        self.session=requests.Session()
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
