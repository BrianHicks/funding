from django.conf.urls.defaults import patterns, url, include

from funding.apps.funding import views

urlpatterns = patterns(
    '',
    url(r'^$', views.BalancedAccountListView.as_view(), name='list'),
    url(r'^bankaccount/add/$', views.BalancedAccountAddView.as_view(), name='add'),
    url(r'^bankaccount/(?P<pk>\d+)/delete/$', views.BalancedAccountDeleteView.as_view(), name='delete'),
)
