from django.conf.urls.defaults import patterns, url, include

from funding.apps.accounts import views

accounts_urls = patterns(
    '',
    url(r'^$', views.FundingListView.as_view(), name='list'),
    url(r'^add/$', views.ReceiverAddAccountView.as_view(), name='add'),
)

urlpatterns = patterns(
    '',
    url(r'^funding/', include(accounts_urls, namespace='funding')),
    url('', include('userena.urls')),
)
