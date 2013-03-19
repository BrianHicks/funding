'views for trips'
from django.views.generic.list import ListView

from .models import Trip
from funding.common.views import LoginRequiredMixin

class TripListView(LoginRequiredMixin, ListView):
    'list of trips'
    model = Trip

    def get_queryset(self):
        'get queryset for this list'
        return Trip.objects.for_user('change', self.request.user)
