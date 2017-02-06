from django.conf.urls import url
from posts.views import AddPostView
from . import views
urlpatterns = [
                  url(r'^$', views.posts, name='posts'),
                  url(r'^add$', AddPostView.as_view(), name='add_post'),
                  url(r'^edit/(?P<post_id>[0-9]+)/$', views.edit_post, name='edit_post'),
                  url(r'^save$', views.save_editions, name='save_editions'),
                  url(r'^delete$', views.delete_post, name='delete_post'),
                  url(r'^make_not_relevant$', views.make_post_not_relevant, name='make_post_not_relevant'),
                  url(r'^like$', views.like_post, name='like_post'),
                  url(r'^who_liked/(?P<post_id>[0-9]+)/$', views.who_liked, name='who_liked'),
                  url(r'^liked/$', views.liked, name='liked'),
              ]
