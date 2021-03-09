from django.shortcuts import render, HttpResponse

# Create your views here.

def home(request):
    # html = '<html><body>首页</body></html>'
    # return HttpResponse(html)

    context = {
        'active_menu': 'home',
    }
    return render(request, 'index.html', context=context)
