# coding=utf-8
from django.contrib import admin
from models import Post
from django.utils import timezone

# post actions
def make_accepted(modeladmin, request, queryset):
	for post in queryset:
		post.accepted = True
		post.accepted_datetime = timezone.now()
		post.save()
make_accepted.short_description = 'Одобрить'

def make_rejected(modeladmin, request, queryset):
	for post in queryset:
		post.rejected = True
		post.save()	
make_rejected.short_description = 'Отвергнуть'
# customize
class PostAdmin(admin.ModelAdmin):

	list_display = (
			'user',
			'text',
			'photo_tag_verbose',
			'pub_datetime',
			'place',
			'tag',
			'is_anonymous',
			'is_actual',
			'accepted',
			'rejected'
	)

	list_select_related = True

	list_filter = ['is_actual', 'accepted', 'rejected', 'place']

	actions = [make_accepted, make_rejected]

	def photo_tag_verbose(self, obj):
		return obj.photos_tags
	photo_tag_verbose.short_description = u'Фото'
# Register your models here.
admin.site.register(Post, PostAdmin)
