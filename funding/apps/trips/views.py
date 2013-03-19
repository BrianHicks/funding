'views for trips'
from django.views.generic.list import ListView

from .models import Trip
from funding.common.views import LoginRequiredMixin

class TripListView(LoginRequiredMixin, ListView):
    'list of trips'
    model = Trip
