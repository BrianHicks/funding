from django.conf.urls.defaults import patterns, url
from .views import HomepageView

urlpatterns = patterns(
    '',
    url('^$', HomepageView.as_view()),
)
