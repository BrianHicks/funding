'urls for trips'
from django.conf.urls.defaults import patterns, url

from funding.apps.trips import views

matchers = {
    'pk': r'(?P<pk>\d+?)'
}

urlpatterns = patterns(
    '',
    url(r'^$', views.TripListView.as_view(), name='list'),
    url(r'^create/$', views.TripCreateView.as_view(), name='create'),
    url(r'^%(pk)s/update/$' % matchers, views.TripUpdateView.as_view(), name='update'),
    url(r'^%(pk)s/delete/$' % matchers, views.TripDeleteView.as_view(), name='delete'),
)
