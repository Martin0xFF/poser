from django.shortcuts import render
from video.models import Session

def index(request):
    context= {}
    return render(request, 'poser/index.html', context)