from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns(
    '',
    url('', include('userena.urls')),
)
