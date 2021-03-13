from django.urls import path
from . import views

app_name = 'newsApp'

urlpatterns = [
    path('news/<str:news_name>/', views.news, name='news'),                 # 新闻列表
    path('newsDetail/id=<int:id>', views.news_detail, name='newsDetail'),   # 新闻详情
    # path('search/', views.search, name='search'),                           # 新闻搜索
]
