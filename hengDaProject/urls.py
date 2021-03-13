"""hengDaProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from homeApp.views import home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),                # 管理员
    path('', home, name='home'),                    # 首页
    path('', include('aboutApp.urls')),     # 公司简介
    path('', include('newsApp.urls')),      # 新闻动态
    path('', include('productsApp.urls')),  # 产品中心
    path('service/', include('serviceApp.urls')),   # 服务支持
    path('', include('scienceApp.urls')),   # 科研基地
    path('contact/', include('contactApp.urls')),   # 人才招聘
    path('ueditor/', include('DjangoUeditor.urls')),    # 富文本插件
    path('search/', include('haystack.urls')),          # 搜索插件
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)