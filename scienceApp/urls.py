from django.urls import path
from . import views

app_name = 'scienceApp'

urlpatterns = [
    path('', views.science, name='science'),   # 科研基地
]
