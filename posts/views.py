from django.shortcuts import render
from django.http import HttpResponse
from posts.models import VK_User, HashBackend

# Create your views here.

def index(request):
    return render(request, 'posts/auth.html', {})

def registration(request):
    vk_user = authenticate(request.GET.get('first_name'), request.GET.get('last_name'), request.GET.get('photo_rec'), request.GET.get('uid'), request.GET.get('hash'))
    if vk_user is not None:
        redirect("specify_point", foo='bar')
    else:
        return HttpResponse("fail")

def spicify_point(request):
    if request.vk_user.is_authenticated():
        return HttpResponse(request.vk_user.first_name + ", " + "specify your city.")
