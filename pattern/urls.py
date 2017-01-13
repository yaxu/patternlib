from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add/$', views.add, name='pattern_add'),
    url(r'^(?P<pk>\d+)/$', views.pattern_detail, name='pattern_detail'),
    url(r'^logout/$', views.logout)
]
