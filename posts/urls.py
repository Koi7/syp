# coding=utf-8
from django.conf.urls import url
from posts.views import AddPostView, Posts, DeletePost, LikePost, WhoLiked, LikedPosts, \
    Profile, LeaveMessage, MyPost, SaveProfileEditions, DeleteUser, PhotoUploader, PostsFilter, Notifications, CloseAttention, About, Contacts, NotificationsAjax

urlpatterns = [
    url(ur'^$', Posts.as_view(), name='posts'),
    url(ur'^новый$', AddPostView.as_view(), name='add_post'),
    url(ur'^удалить$', DeletePost.as_view(), name='delete_post'),
    url(ur'^лайк$', LikePost.as_view(), name='like_post'),
    url(ur'^послание$', LeaveMessage.as_view(), name='leave_message'),
    url(ur'^нравится$', WhoLiked.as_view(), name='who_liked'),
    url(ur'^мне_понравилось$', LikedPosts.as_view(), name='liked'),
    url(ur'^изменить/$', SaveProfileEditions.as_view(), name='save_profile_editions'),
    url(ur'^профиль$', Profile.as_view(), name='profile'),
    url(ur'^мой$', MyPost.as_view(), name='my_posts'),
    url(ur'^профиль/удалить$', DeleteUser.as_view(), name='delete_user'),
    url(ur'^загрузить$', PhotoUploader.as_view(), name='upload_photo'),
    url(ur'^удалить_фото(?:/(?P<qquuid>\S+))?', PhotoUploader.as_view(), name='delete_photo'),
    url(ur'^фильтр$', PostsFilter.as_view(), name='posts_filter'),
    url(ur'^уведомления$', Notifications.as_view(), name='notifications'),
    url(ur'^уведомления/еще$', NotificationsAjax.as_view(), name='notifications_ajax'),
    url(ur'^предупрежден$', CloseAttention.as_view(), name='close_attention'),
]
