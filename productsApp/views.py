from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Product
from django.core.paginator import Paginator

# Create your views here.


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    product.views += 1
    product.save()

    return render(request, 'productDetail.html', {
        'active_menu': 'products',
        'product': product,
    })


def products(request, product_name):
    sub_menu = product_name

    product_list = Product.objects.filter(
        product_type=product_name).order_by('-publish_date')
    paginator = Paginator(product_list, 2)

    if paginator.num_pages <= 1:
        page_data = ''
    else:
        page = int(request.GET.get('page', 1))
        if page < 1:
            page = 1
        elif page > paginator.num_pages:
            page = paginator.num_pages
        product_list = paginator.page(page)
        page_data = get_page_data(paginator, page)

    if product_name == 'robot':
        product_name = '家用机器人'
    elif product_name == 'monitoring':
        product_name = '智能监控'
    elif product_name == 'face':
        product_name = '人脸识别解决方案'

    context = {
        'active_menu': 'products',
        'sub_menu': sub_menu,
        'product_name': product_name,
        'product_list': product_list,
        'page_data': page_data,
    }
    return render(request, 'productList.html', context=context)


def get_page_data(paginator, page):
    total_pages = paginator.num_pages
    page_range = paginator.page_range
    first = False   # 是否需要显示第一页
    last = False    # 是否需要显示最后一页
    left_has_more = False
    right_has_more = False

    left_ind = (page-3) if page-3 > 0 else 0
    left = page_range[left_ind: page-1]
    right = page_range[page: page+2]

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
        'first': first,
        'last': last,
        'left_has_more': left_has_more,
        'right_has_more': right_has_more,
    }
