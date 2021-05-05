import cv2, requests

url = 'http://192.168.1.101:8000/service/api/facedetect/'

# 上传图像并检测
tracker = None
img_path = 'face.jpg'
files = {
    'image': ('filename2', open(img_path, 'rb'), 'image/jpeg'),
}

res = requests.post(url, data=tracker, files=files).json()
print(f'获取信息: {res}')

# 将检测结果框显示在图像上
img = cv2.imread(img_path)
for x1, y1, x2, y2 in res['faces']:
    img = cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

cv2.imwrite('facedetect.png', img)
cv2.imshow('face detection', img)
cv2.waitKey(0)
