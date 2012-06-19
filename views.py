# -*- coding: utf-8 -*-

__author__ = 'Francisco Perez <francofuji@gmail.com>'

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.

from django.contrib.contenttypes.models import ContentType

from forms import Form_SetRights

def set_rights(request, ):
	'''
	This view get the id(s) and the content type of selected entities in the change list
	screen of some registered content type and pass them to the FormSetRight form
	'''
	ct = ContentType.objects.get(pk = int(request.GET.get('ct')))

	ids = request.GET.get('ids')

	form = Form_SetRights(request.POST or None)
	if form.is_valid():
		form.save(ct, ids)
		return HttpResponseRedirect('/admin')

	params = {}
	params['pp_label'] = ct.app_label
	params['model'] = ct.model_class()
	params['form'] = form

	return render_to_response('admin/set_rights.html', params, RequestContext(request))

