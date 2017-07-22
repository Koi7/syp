# coding=utf-8
from django.contrib import admin
from models import Post, VKUser, BlackList, PostImage, Ad
from django.utils import timezone
from django.contrib.auth.models import Group

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

class PostImageAdmin(admin.ModelAdmin):

	list_display = (
			'user',
			'post',
			'image_tag',
			'has_post'
	)

	list_select_related = True

	list_filter = ['has_post']
	def get_image_tag(self, obj):
			return obj.image_tag
	get_image_tag.short_description = 'Фото'

class AdAdmin(admin.ModelAdmin):

	list_display = (
			'brand',
			'brand_icon_as_image',			
			'brand_ofsite_as_link',
			'place',
			'text',
			'pub_datetime',
			'days',
			'accepted',
			'is_active',
			'get_images_tags'
	)

	list_select_related = True

	list_filter = ['accepted', 'place']

	def get_images_tags(self, obj):
			return obj.images_as_tags
	get_images_tags.short_description = 'Фото'
	def is_active(self, obj):
			return obj.is_active
	is_active.short_description = 'Активна?'
	def brand_ofsite_as_link(self, obj):
			return obj.brand_ofsite_as_link
	brand_ofsite_as_link.short_description = 'Офсайт'
	def brand_icon_as_image(self, obj):
			return obj.brand_icon_as_image
	brand_icon_as_image.short_description = 'Лого'

# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(VKUser, VKUserAdmin)
admin.site.register(BlackList, BlackListAdmin)
admin.site.register(PostImage, PostImageAdmin)
admin.site.register(Ad, AdAdmin)
admin.site.unregister(Group)
