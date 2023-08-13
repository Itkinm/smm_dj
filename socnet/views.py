from django.shortcuts import render

# Create your views here.

from django.shortcuts import get_object_or_404, render
from django.http import Http404

from django.http import HttpResponse
from django.template import loader
from socnet.models import Platform, Page, Shtab
# Create your views here.

def index(request):
    return render(request, 'socnet/index.html')


def platform(request, platform_name):
    print (platform_name)
    platforms_dict = {v: k for k, v in Platform.NAME_CHOICES}
    try:
        platform_name = platforms_dict[platform_name]
    except:
        raise Http404("Nothing to see here")
    platform = get_object_or_404(Platform, name=platform_name)
    return render(request, 'socnet/platform/platform.html', {'platform': platform})   

def shtab(request, shtab_name):   
    shtab = Page.objects.get(platform=Platform.SI, username = shtab_name).shtab
    return render(request, 'socnet/shtab/shtab.html', {'shtab': shtab}) 