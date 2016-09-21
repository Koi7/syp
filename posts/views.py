from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import logout
from posts.models import HashBackend
# Create your views here.
def anonimous_check(user):
    return  user.is_anonymous()
@user_passes_test(anonimous_check, login_url='/posts')
def index(request):
    return render(request, 'posts/auth.html', {})

@user_passes_test(anonimous_check, login_url='/posts')
def verify_hash(request):
    hash_backend = HashBackend()
    user = HashBackend.authenticate(hash_backend, request.GET.get('uid'), request.GET.get('hash'))
    if user is not None:
        user.first_name = request.GET.get('first_name')
        user.last_name = request.GET.get('last_name')
        user.photo_rec = request.GET.get('photo_rec')
        user.save()
        login(request, user)
        return redirect('../posts')
    else:
        return redirect('../?login=fail')

@login_required
def posts(request):
    context = {
        'first_name': request.user.first_name
    }
    return render(request, 'posts/posts.html', context)

def logout_view(request):
    logout(request)
    return redirect('../')
