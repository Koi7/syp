from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.posts, name='posts'),
    url(r'^add', views.add_post, name='add_post'),
    url(r'^edit/?(<post_id>)[0-9]]+/', views.edit_post, name='edit_post'),
    url(r'^save', views.save_editions, name='save_editions'),
    url(r'^delete', views.delete_post, name='delete_post'),
    url(r'^make_not_relevant', views.make_post_not_relevant, name='make_post_not_relevant'),
    url(r'^like', views.like_post, name='like_post'),
    url(r'^liked/?(<post_id>)[0-9]]+/', views.liked, name='liked'),
]