from django.shortcuts import render, HttpResponse

# Create your views here.

def science(request):
    # html = '<html><body>科研基地</body></html>'
    # return HttpResponse(html)

    context = {
        'active_menu': 'science',
    }
    return render(request, 'science.html', context=context)
