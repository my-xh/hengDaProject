# -*- coding: utf-8 -*-

"""
@File    : ocr_detect_demo.py
@Time    : 2021/5/5 13:38
@Author  : my-xh
@Version : 1.0
@Software: PyCharm
@Desc    : 
"""

import requests

url = 'http://192.168.1.101:8000/service/api/ocrdetect/'

# 上传图像并检测
tracker = None
img_path = 'ocrtest.png'
files = {
    'image': ('filename2', open(img_path, 'rb'), 'image/jpeg')
}

res = requests.post(url, data=tracker, files=files).json().get('code')

# 显示识别内容
if res:
    print(f'识别结果:\n{res.strip()}')
else:
    print('识别失败！')
