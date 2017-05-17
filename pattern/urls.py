from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.pattern_index, name='index'),
    url(r'^add/$', views.pattern_edit, name='pattern_add'),
    url(r'^person/(?P<ident>\w+)/$', views.pattern_person, name='pattern_person'),
    url(r'^(?P<pk>\d+)/$', views.pattern_detail, name='pattern_detail'),
    url(r'^(?P<pk>\d+)/edit/$', views.pattern_edit, name='pattern_edit'),
    url(r'^(?P<parent_pk>\d+)/progress$', views.pattern_edit, name='pattern_progress'),
    url(r'^(?P<pk>\d+)/love/$', views.pattern_love, name='pattern_love'),
    url(r'^(?P<pk>\d+)/unlove/$', views.pattern_unlove, name='pattern_unlove'),
    url(r'^logout/$', views.logout)
]
