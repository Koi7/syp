# coding=utf-8
from django.contrib import admin
from models import Post, VKUser, BlackList
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
			'text',
			'photo_tag_verbose',
			'pub_datetime',
			'place',
			'tag',
			'is_anonymous',
			'accepted',
			'rejected'
	)

	list_select_related = True

	list_filter = ['accepted', 'rejected', 'place']

	actions = [make_accepted, make_rejected]

	def photo_tag_verbose(self, obj):
		return obj.photos_tags
	photo_tag_verbose.short_description = u'Фото'

class VKUserAdmin(admin.ModelAdmin):

	list_display = (
			'get_fname',
			'get_lname',
			'get_photo',
			'get_place',
			'age',
			'sex',
	)

	def get_fname(self, obj):
		return obj.user.first_name
	get_fname.short_description = 'Имя'
	def get_lname(self, obj):
		return obj.user.last_name
	get_lname.short_description = 'Фамилия'
	def get_photo(self, obj):
		return obj.photo
	get_photo.short_description = 'Фото'
	def get_place(self, obj):
		return obj.place_str
	get_place.short_description = 'Город'

class BlackListAdmin(admin.ModelAdmin):

	list_display = (
			'vk_id',
			'timestamp',
			'days',
			'get_state',
	)

	def get_state(self, obj):
		return obj.is_active
	get_state.short_description = 'Действительно?'
# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(VKUser, VKUserAdmin)
admin.site.register(BlackList, BlackListAdmin)
