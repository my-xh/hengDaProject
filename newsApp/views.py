from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import MyNews
from django.core.paginator import Paginator
from pyquery import PyQuery as pq

# Create your views here.

def search(request):
    keyword = request.GET.get('keyword')
    news_list = MyNews.objects.filter(title__icontains=keyword)
    news_name = f'关于 "{keyword}" 的搜索结果'
    return render(request, 'searchList.html', {
        'active_menu': 'news',
        'news_name': news_name,
        'news_list': news_list,
    })


def news_detail(request, id):
    my_news = get_object_or_404(MyNews, id=id)
    my_news.views += 1
    my_news.save()

    return render(request, 'newsDetail.html', {
        'active_menu': 'news',
        'my_news': my_news,
    })

def news(request, news_name):
    sub_menu = news_name
    news_list = MyNews.objects.filter(news_type=news_name).order_by('-publish_date')

    pgnt = Paginator(news_list, 5)

    if pgnt.num_pages <= 1:
        page_data = ''
    else:
        page = int(request.GET.get('page', 1))
        if page < 1:
            page = 1
        elif page > pgnt.num_pages:
            page = pgnt.num_pages
        news_list = pgnt.get_page(page)
        page_data = get_page_data(pgnt, page)

    if news_name == 'company':
        news_name = '企业要闻'
    elif news_name == 'industry':
        news_name = '行业新闻'
    elif news_name == 'notice':
        news_name = '通知公告'

    for my_news in news_list:
        html = pq(my_news.description)
        # print(html)
        my_news.my_txt = html('p').text()

    return render(request, 'newsList.html', {
        'active_menu': 'news',
        'sub_menu': sub_menu,
        'news_name': news_name,
        'news_list': news_list,
        'page_data': page_data,
    })


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