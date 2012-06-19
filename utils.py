# -*- coding: utf-8 -*-

__author__ = 'Francisco Perez <francofuji@gmail.com>'

from django.contrib.contenttypes.models import ContentType

from models import Content_Object_Right, Content_Type_Registration

def get_right(content_object):
	'''
	Recursive function that look for the right of a given content object.
	'''
	content_type = ContentType.objects.get_for_model(content_object)
	try:
		content_right = Content_Object_Right.objects.get(content_type__pk=content_type.id, object_id = content_object.id)
		return content_right.right.short_name
	except:
		try:
			content_type_registration = Content_Type_Registration.objects.get(content_type = content_type)
			return get_right(getattr(content_object, content_type_registration.parent_field_name))
		except:
			return None

