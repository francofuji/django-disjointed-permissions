# -*- coding: utf-8 -*-

__author__ = 'Francisco Perez <francofuji@gmail.com>'

from django.conf.urls.defaults import *


urlpatterns = patterns('apps.permissions.views',
	(r'^set_rights/$', 'set_rights'),
	(r'^test_view/$', 'test_view'),
)
