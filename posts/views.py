from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout
from posts.models import HashBackend
from django.conf import settings

# User tests.
def anonimous_check(user):
    return  user.is_anonymous()

# Create your views here.
@user_passes_test(anonimous_check, login_url='/posts')
def index(request):
    """
        View for default page of unlogged user.
    """
    return render(request, 'posts/auth.html', {'run': 56})

@user_passes_test(anonimous_check, login_url='/posts')
def verify_hash(request):
    """
        Takes URL from vk.com redirect and tryes to login user or create new user.
        Checks md5 checksum.
    """
    hash_backend = HashBackend()
    user = HashBackend.authenticate(hash_backend, request.GET.get('uid'), request.GET.get('hash'))
    if user is not None:
        user.first_name = request.GET.get('first_name')
        user.last_name = request.GET.get('last_name')
        user.vkuser.photo_rec = request.GET.get('photo_rec')
        user.save()
        login(request, user)
        return redirect('../posts')
    else:
        return redirect('../?login=fail')

@login_required
def posts(request):
    """
        View for default page of logged user.
    """
    return render(request, 'posts/posts.html')

def logout_view(request):
    logout(request)
    return redirect('../')
