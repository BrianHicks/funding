'urls for trips'
from django.conf.urls.defaults import patterns, url

from funding.apps.trips import views

urlpatterns = patterns(
    '',
    url(r'^$', views.TripListView.as_view(), name='list'),
)
