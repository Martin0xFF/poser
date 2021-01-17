from django.shortcuts import render
from django.http import StreamingHttpResponse
from camera import VideoCamera, pn_gen
from .models import Session

def index(request):
    seshs = Session.objects.order_by('-sesh_date')
    context={"seshs": seshs}
    return render(request, 'video/index.html', context)

def new_session(request):
    s = Session(session_id="Swagger")
    s.save()
    return phys_session(request, s.pk)

def phys_session(request, session_id):
    seshs = Session.objects.order_by('-sesh_date')[:5]
    context = {
        "session_id": session_id,
        "seshs" : seshs,
    }
    return render(request, 'video/phys_session.html', context)

def _dance(request):
    context={}
    return StreamingHttpResponse(pn_gen(VideoCamera()), content_type='multipart/x-mixed-replace; boundary=frame')