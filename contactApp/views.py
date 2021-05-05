from django.shortcuts import render, HttpResponse
from .models import Ad
from .forms import ResumeForm

# Create your views here.

def contact(request):
    return render(request, 'contact.html', {
        'active_menu': 'contact',
        'sub_menu': 'contactus',
    })

def recruit(request):
    ad_list = Ad.objects.all().order_by('-publish_date')
    if request.method == 'POST':
        resume_form = ResumeForm(data=request.POST, files=request.FILES)
        if resume_form.is_valid():
            resume_form.save()
            return render(request, 'success.html', {
                'active_menu': 'contact',
                'sub_menu': 'recruit',
            })
    else:
        resume_form = ResumeForm()
    return render(request, 'recruit.html', {
        'active_menu': 'contact',
        'sub_menu': 'recruit',
        'AdList': ad_list,
        'resumeForm': resume_form,
    })
