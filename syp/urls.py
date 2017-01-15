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
from django.contrib import admin
from posts import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login', views.verify_hash, name='verify_hash'),
    url(r'^specify_place', views.specify_place, name='specify_place'),
    url(r'^admin', admin.site.urls),
    url(r'^posts/', include('posts.urls')),
    url(r'^logout', views.logout_view, name='logout_view'),
]

handler404 = 'posts.views.not_found'
