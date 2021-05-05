from django.urls import path
from . import views

app_name = 'serviceApp'

urlpatterns = [
    path('service/download/', views.download, name='download'),                     # 资料下载列表
    path('download/<int:id>', views.get_doc, name='getDoc'),                        # 下载资料
    path('service/platform/', views.platform, name='platform'),                     # 人脸识别开放平台
    path('service/api/facedetect/', views.facedetect, name='facedetect'),           # 人脸检测API
    path('service/facedetect_demo', views.facedetect_demo, name='facedetect_demo'), # 在线人脸检测
    path('service/ocr', views.ocr, name='ocr'),                                     # 中文字符识别开放平台
    path('service/api/ocrdetect/', views.ocrdetect, name='ocrdetect'),              # 中文字符识别API
]
