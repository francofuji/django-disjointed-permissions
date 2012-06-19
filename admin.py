# -*- coding: utf-8 -*-

__author__ = 'Francisco Perez <francofuji@gmail.com>'


from django.http import HttpResponseRedirect
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin

from models import Content_Type_Registration, Right, Content_Object_Right


class AdminRights(admin.ModelAdmin):
	list_display = ('short_name', 'long_name')

class AdminContentObjectRight(admin.ModelAdmin):
	list_display = ('object_with_right', 'right')

	def object_with_right(self, obj):
		return '%s - [%s]' % (obj.content_object.__unicode__(), obj.content_type.model_class().__name__)

class AdminRegisteredContents(admin.ModelAdmin):
	'''
	ModelAdmin for registered models. It means models with rights
	'''

	actions = ['set_rights']

	def set_rights(self, request, queryset):
		selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
		ct = ContentType.objects.get_for_model(queryset.model)
		return HttpResponseRedirect("/rights/set_rights/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))
	set_rights.short_description = "Set rights for selected objects"

class AdminUser(UserAdmin, AdminRegisteredContents):
	pass

class AdminGroup(GroupAdmin, AdminRegisteredContents):
	pass

registered_content_types = Content_Type_Registration.objects.all()

for registered_contenttype in registered_content_types:
	admin.site.unregister(registered_contenttype.content_type.model_class())

	if registered_contenttype.content_type.model_class() == User:
		admin.site.register(registered_contenttype.content_type.model_class(), AdminUser)
		continue
	if registered_contenttype.content_type.model_class() == Group:
		admin.site.register(registered_contenttype.content_type.model_class(), AdminGroup)
		continue

	admin.site.register(registered_contenttype.content_type.model_class(), AdminRegisteredContents)

admin.site.register(Content_Type_Registration)
admin.site.register(Right, AdminRights)
admin.site.register(Content_Object_Right, AdminContentObjectRight)
