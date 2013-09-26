#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Frank'

from django.conf.urls import patterns, url

from SGIAPP import views

# Aquí se hace el mapping de url contra acción, y se nombra la url
urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^login$', views.login, name='login'),
    url(r'^register$', views.register, name='register'),
    url(r'^doreg$', views.doregistration, name='doregistration'),
    url(r'^incidences$', views.userilist, name='userilist'),
    url(r'^report_incidence$', views.incidence_report, name='report_incidence'),
    url(r'^do_report$', views.do_report, name='do_report'),
    url(r'^incidence/(?P<pk>\d+)/$', views.IncidencesDetailView.as_view(), name='incidence_detail'),
    url(r'^check$', views.check_for_entity_incidences, name='check_incidences'),
    url(r'^confirm/(?P<id>\d+)/$', views.confirm, name='confirm'),
    url(r'^finish/(?P<id>\d+)/$', views.finish, name='finish'),
    url(r'^dofinish$', views.do_finish, name='do_finish'),
    url(r'^logout$', views.logout, name='logout'),

)