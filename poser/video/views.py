from django.shortcuts import render
from django.http import StreamingHttpResponse
from camera import VideoCamera, pn_gen
def index(request):
    context={}
    # some other data
    return render(request, 'video/index.html', context)

def dance(request):

    context={}
    return StreamingHttpResponse(pn_gen(VideoCamera()), content_type='multipart/x-mixed-replace; boundary=frame')