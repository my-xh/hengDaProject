from django.shortcuts import render, HttpResponse

from django.db.models import Q
from newsApp.models import MyNews
from productsApp.models import Product

from django.views.decorators.cache import cache_page

# Create your views here.

@cache_page(60 * 15)    #每15分钟缓存一次
def home(request):
    news_list = MyNews.objects.filter(~Q(news_type="notice")).order_by('-publish_date')
    note_list = MyNews.objects.filter(Q(news_type="notice")).order_by('-publish_date')
    product_list = Product.objects.all().order_by('-views')
    post_list, post_num = [], 0
    for s in news_list:
        if s.photo:
            post_list.append(s)
            post_num += 1
        if post_num == 3:
            break
    
    news_list = news_list[:7]
    note_list = note_list[:4]
    product_list = product_list[:4]

    context = {
        'active_menu': 'home',
        'newsList': news_list,
        'postList': post_list,
        'noteList': note_list,
        'productList': product_list,
    }
    return render(request, 'index.html', context=context)
