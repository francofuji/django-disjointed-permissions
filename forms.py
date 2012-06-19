# -*- coding: utf-8 -*-

__author__ = 'Francisco Perez <francofuji@gmail.com>'

from django import forms

from models import Right, Content_Object_Right

class Form_SetRights(forms.Form):
	'''
	This form saves the right assigned to selected objects in admin.
	'''
	right = forms.ModelChoiceField(queryset=Right.objects.all())

	def save(self, content_type, ids):
		right = self.cleaned_data['right']
		ids = ids.split(',')
		model_class = content_type.model_class()
		for id in ids:
			content_object = model_class.objects.get(pk = int(id))
			contentright = Content_Object_Right(content_object=content_object, right = right)
			contentright.save()
