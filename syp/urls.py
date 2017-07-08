# coding=utf-8
"""syp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from posts.views import IndexView, About, Contacts, logout_view
from syp import settings

urlpatterns = [
    url(ur'^$', IndexView.as_view(), name='index'),
    url(ur'^вход', IndexView.as_view(), name='index'),
    url(ur'^па/', admin.site.urls),
    url(ur'^посты/', include('posts.urls')),
    url(ur'^выход', logout_view, name='logout_view'),
    url(ur'^проект$', About.as_view(), name='about'),
    url(ur'^контакты$', Contacts.as_view(), name='contacts'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'posts.views.not_found'
