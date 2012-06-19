# -*- coding: utf-8 -*-

__author__ = 'Francisco Perez <francofuji@gmail.com>'

from django.db import models

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class Right(models.Model):
	'''
	This model holds all available rights
	'''
	short_name = models.CharField(max_length=20, unique=True)
	long_name = models.CharField(max_length=100, blank=True, null=True)

	def __unicode__(self):
		return (self.long_name or '[%s]' % self.short_name)

class Content_Object_Right(models.Model):
	'''
	This model holds the relation betwen any content object and some right.
	Using the contenttype application allow to assign a right to any object from any model.
	A content object can have only one right assigned to it.
	That is because in pythie the defined rights are mutually disjointed.
	'''
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	content_object = generic.GenericForeignKey('content_type', 'object_id')
	right = models.ForeignKey(Right)

	class Meta:
		unique_together = ('content_type', 'object_id')
		verbose_name = "Object right"

class Content_Type_Registration(models.Model):
	'''
	This model holds hierarchy relations betwen content types.
	In some case where some content object don't have any right
	assigned directly to it, this model could allow to look for some
	 parent model with a right assigned. The content object right will
	 be the first found in the parent models hierarchy.
	'''
	content_type = models.ForeignKey(ContentType, unique=True)
	parent_content_type = models.ForeignKey(ContentType, related_name='childs', null=True, blank=True)
	parent_field_name = models.CharField(max_length=50, blank=True, null=True)

	def __unicode__(self):
		return self.content_type.model.capitalize()

	class Meta:
		verbose_name = "Content type registration"

	@classmethod
	def register_content_type(cls, *args):
		'''
		Accept a secuence of tuples with three items equivalentes to a record
		in the model.
		'''
		for arg in args:
			if arg.__class__.__name__ != 'tuple':
				raise Exception
			else:
				params = {}
				params['content_type'] = ContentType.objects.get_for_model(arg[0])
				if len(arg) > 1:
					params['parent_content_type'] = ContentType.objects.get_for_model(arg[1])
					params['parent_field_name'] = arg[2]
				ctr = cls.objects.create(**params)





