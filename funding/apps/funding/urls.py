from django.conf.urls.defaults import patterns, url, include

from funding.apps.funding import views

urlpatterns = patterns(
    '',
    url(r'^$', views.FundingListView.as_view(), name='list'),
    url(r'^add/$', views.ReceiverAddAccountView.as_view(), name='add'),
)
