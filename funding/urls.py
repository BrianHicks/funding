from django.contrib import admin
from django.conf.urls.defaults import patterns, include, url


# See: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#hooking-adminsite-instances-into-your-urlconf
admin.autodiscover()


# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = patterns(
    '',
    # Admin panel and documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^funding/', include('apps.funding.urls', namespace='funding')),
    url(r'^trips/', include('apps.trips.urls', namespace='trips')),

    url(r'^account/', include('account.urls')),

    # put static last
    url(r'^', include('apps.static.urls', namespace='static')),
)
