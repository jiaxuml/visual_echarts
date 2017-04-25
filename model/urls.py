#coding:utf-8

from django.conf.urls import url

from model import views

urlpatterns = [
		url(r'^zfmc/$',views.zfmc, name='zfmc'),
	    url(r'^zfmc/1/$', views.zfmcshow1, name='zfmcshow'),
        url(r'^zfmc/2/$', views.zfmcshow2, name='zfmcshow'),
        url(r'^zfmc/3/$', views.zfmcshow3, name='zfmcshow'),
		]
