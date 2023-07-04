from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^stihi/$', views.StihListView.as_view(), name='stihi'),
    url(r'^stih/(?P<pk>\d+)$', views.StihDetailView.as_view(), name='stih-detail'),
    url(r'^authors/$', views.AuthorListView.as_view(), name='authors'),
    url(r'^author/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author-detail'),
]

urlpatterns += [
    url(r'^mystihs/$', views.StihsByUserListView.as_view(), name='my-stihs'),
    url(r'^uncheckedstihs/$', views.UncheckedStihsListView.as_view(), name='unchecked-stihs'),
    url(r'^stih/(?P<pk>[-\w]+)/renew/$', views.renew_stih, name='renew-stih'),

	url(r'^author/create/$', views.AuthorCreate.as_view(), name='author_create'),
    url(r'^author/(?P<pk>\d+)/update/$', views.AuthorUpdate.as_view(), name='author_update'),
    url(r'^author/(?P<pk>\d+)/delete/$', views.AuthorDelete.as_view(), name='author_delete'),

    url(r'^stih/create/$', views.StihCreate.as_view(), name='stih_create'),
    url(r'^stih/user-create/$', views.StihUserCreate.as_view(), name='stih_user_create'),
    url(r'^stih/(?P<pk>\d+)/update/$', views.StihUpdate.as_view(), name='stih_update'),
    url(r'^stih/(?P<pk>\d+)/delete/$', views.StihDelete.as_view(), name='stih_delete'),

    url(r'^register/$', views.register, name='register'),
]