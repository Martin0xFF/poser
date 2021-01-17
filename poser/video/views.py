from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponse, JsonResponse
from camera import VideoCamera, pn_gen
from .models import Session
from django.views.decorators.csrf import csrf_exempt
from queue import Queue
import json
import cv2
import Scorer
import base64
import re
import numpy as np
sc = Scorer.Scorer()
q = Queue()


@csrf_exempt
def update_score(request):
    sesh = Session.objects.latest('-sesh_date')
    res = {}
    if request.method == 'POST':
        seshs = Session.objects.order_by('-sesh_date')
        data_dict = json.loads(request.body)

        if "value" in data_dict and "tar_value" in data_dict:
            im_bytes = base64.b64decode(data_dict['value'].split(',')[1])
            im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
            src_f = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

            im_bytes = base64.b64decode(data_dict['tar_value'].split(',')[1])
            im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
            tar_f = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
            err, overlay = sc.score_poses(src_f, tar_f)

            #score = 1/(1 + err)
            #sesh.score = sesh.score*0.5 + score*0.5
            #sesh.save()

            retval, buffer = cv2.imencode('.jpg', overlay)
            jpg_as_text = base64.b64encode(buffer)

            res = {
                "score": sesh.score,
                "overlay": jpg_as_text
            }
            q.put(res)

    return HttpResponse("Exaggerated Swagger of a Software Developer")

def collect(request):
    out = {}
    if request.method == 'GET':
        if q.empty() == False:
            out = q.get()
    return JsonResponse(out)

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