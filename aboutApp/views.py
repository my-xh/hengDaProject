from django.shortcuts import render, HttpResponse
from .models import Award
# Create your views here.

def survey(request):
    # html = '<html><body>企业概况</body></html>'
    # return HttpResponse(html)
    
    context = {
        'active_menu': 'about',
        'sub_menu': 'survey',
    }
    return render(request, 'survey.html', context=context)

def honor(request):
    # html = '<html><body>荣誉资质</body></html>'
    # return HttpResponse(html)

    awards = Award.objects.all()
    context = {
        'active_menu': 'about',
        'sub_menu': 'honor',
        'awards': awards,
    }
    return render(request, 'honor.html', context=context)
