from django.conf.urls.defaults import patterns, url, include

from funding.apps.funding import views

urlpatterns = patterns(
    '',
    url(r'^add/$', views.BankAccountAddView.as_view(), name='add'),
    url(r'^$', views.BankAccountListView.as_view(), name='list'),
)
