'urls for trips'
from django.conf.urls.defaults import patterns, url

from funding.apps.trips import views

matchers = {
    'pk': r'(?P<pk>\d+?)'
}

urlpatterns = patterns(
    '',
    # endpoints for groups/creation
    url(r'^$', views.TripListView.as_view(), name='list'),
    url(r'^create/$', views.TripCreateView.as_view(), name='create'),

    # endpoints for an individual trip
    url(r'^%(pk)s/$' % matchers, views.TripDetailView.as_view(), name='detail'),
    url(r'^%(pk)s/update/$' % matchers, views.TripUpdateView.as_view(), name='update'),
    url(r'^%(pk)s/delete/$' % matchers, views.TripDeleteView.as_view(), name='delete'),
)
