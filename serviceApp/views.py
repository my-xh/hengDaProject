import pytesseract
from PIL import Image
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Doc
from django.core.paginator import Paginator

import os
import cv2
import numpy as np
import base64

face_detector_path = r'serviceApp\haarcascade_frontalface_default.xml'
face_detector = cv2.CascadeClassifier(face_detector_path)


# Create your views here.


def download(request):
    doc_list = Doc.objects.all().order_by('-publish_date')
    pgnt = Paginator(doc_list, 5)

    if pgnt.num_pages <= 1:
        page_data = ''
    else:
        page = int(request.GET.get('page', 1))
        if page < 1:
            page = 1
        elif page > pgnt.num_pages:
            page = pgnt.num_pages
        doc_list = pgnt.get_page(page)
        page_data = get_page_data(pgnt, page)

    return render(request, 'docList.html', {
        'active_menu': 'service',
        'sub_menu': 'download',
        'doc_list': doc_list,
        'page_data': page_data,
    })


def get_doc(request, id):
    doc = get_object_or_404(Doc, id=id)

    root = os.getcwd()
    upload_to, file_name = str(doc.file).split('/')
    file_path = os.path.join(root, 'media', upload_to, file_name)

    response = StreamingHttpResponse(read_file(file_path, 512))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = f'attachment;filename="{file_name}"'

    return response


def platform(request):
    return render(request, 'platform.html', {
        'active_menu': 'service',
        'sub_menu': 'platform',
    })


@csrf_exempt
def facedetect(request):
    result = {}
    if request.method == 'POST':
        if request.FILES.get('image', None) is not None:
            img = read_image(stream=request.FILES['image'])
        else:
            result.update({
                '#faceNum': -1,
            })
            return JsonResponse(result)

        if img.shape[2] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_detector.detectMultiScale(
            img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

        # 获取左上角和右下角坐标，并转换成int类型
        faces = [(int(x), int(y), int(x + w), int(y + h))
                 for x, y, w, h in faces]

        result.update({
            '#faceNum': len(faces),
            'faces': faces,
        })

    return JsonResponse(result)


# 在线人脸检测
@csrf_exempt
def facedetect_demo(request):
    result = {}
    if request.method == 'POST':
        if request.FILES.get('image', None) is not None:
            img = read_image(stream=request.FILES['image'])
        else:
            result['#faceNum'] = -1
            return JsonResponse(result)

        if img.shape[2] == 3:
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            img_gray = img

        faces = face_detector.detectMultiScale(
            img_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

        for x, y, w, h in faces:
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        retval, buf_img = cv2.imencode('.jpg', img)  # 在内存中编码为jpg格式
        img64 = base64.b64encode(buf_img)  # base64编码用于网络传输
        img64 = str(img64, encoding='utf-8')  # bytes类型转换为str类型
        result['img64'] = img64

        return JsonResponse(result)


def ocr(request):
    return render(request, 'ocr.html', {
        'active_menu': 'service',
        'sub_menu': 'ocr',
    })


@csrf_exempt
def ocrdetect(request):
    result = {'code': None}
    if request.method == 'POST':
        if request.FILES.get('image', None) is not None:
            img = read_image(stream=request.FILES['image'])
            img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            code = pytesseract.image_to_string(img, lang='chi_sim')
            result.update({'code': code})

    return JsonResponse(result)


# 基于数据流的图像读取
def read_image(stream=None):
    data_temp = stream.read() if stream is not None else b''
    img = np.asarray(bytearray(data_temp), dtype='uint8')
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    return img


# 分批读取文件
def read_file(file_name, buf_size):
    with open(file_name, 'rb') as f:
        while True:
            content = f.read(buf_size)
            if content:
                yield content
            else:
                break


def get_page_data(pgnt, page):
    total_pages = pgnt.num_pages
    left_has_more = False
    right_has_more = False
    first = False
    last = False
    page_range = pgnt.page_range

    left_ind = page - 3 if page - 3 > 0 else 0
    left = page_range[left_ind: page - 1]
    right = page_range[page: page + 2]

    if page > 3:
        first = True
        if page > 4:
            left_has_more = True
    if page < total_pages - 2:
        last = True
        if page < total_pages - 3:
            right_has_more = True

    return {
        'page': page,
        'total_pages': total_pages,
        'left': left,
        'right': right,
        'left_has_more': left_has_more,
        'right_has_more': right_has_more,
        'first': first,
        'last': last
    }
