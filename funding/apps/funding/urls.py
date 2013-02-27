from django.conf.urls.defaults import patterns, url, include

from funding.apps.funding import views

urlpatterns = patterns(
    '',
    url(r'^/$', views.BankAccountListView.as_view(), name='list'),
    url(r'^bankaccount/add/$', views.BankAccountAddView.as_view(), name='add'),
    url(r'^bankaccount/(?P<pk>\d+)/delete/$', views.BankAccountDeleteView.as_view(), name='delete'),
)
