from django.conf.urls import url
from poetries import views


urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^poetries/$',views.PoetryListView.as_view(),name='poetry_list'),
    url(r'^poetry/(?P<pk>\d+)$',views.PoetryDetailView.as_view(),name='poetry_detail'),
    url(r'^poetry/new/$', views.CreatePoetryView.as_view(), name='poetry_new'),
    url(r'^poetry/(?P<pk>\d+)/edit/$', views.PoetryUpdateView.as_view(), name='poetry_edit'),
    url(r'^drafts/$', views.DraftListView.as_view(), name='poetry_draft_list'),
    url(r'^poetry/(?P<pk>\d+)/remove/$', views.PoetryDeleteView.as_view(), name='poetry_remove'),
    url(r'^poetry/(?P<pk>\d+)/publish/$', views.poetry_publish, name='poetry_publish'),
    url(r'^poetry/(?P<pk>\d+)/comment/$', views.add_comment_to_poetry, name='add_comment_to_poetry'),
    url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
]
