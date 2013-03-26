'views for trips'
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from .forms import TripForm
from .models import Trip
from funding.common.views import LoginRequiredMixin

class TripListView(LoginRequiredMixin, ListView):
    'list of trips'
    model = Trip

    def get_queryset(self):
        'get queryset for this list'
        return Trip.objects.for_user('change', self.request.user)


class TripCreateView(LoginRequiredMixin, CreateView):
    'create a new trip'
    model = Trip
    form_class = TripForm
    success_url = reverse_lazy('trips:list')

    def get_form_kwargs(self):
        'get data to pass to TripForm'
        kwargs = super(TripCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class TripUpdateView(LoginRequiredMixin, UpdateView):
    'edit an existing trip'
    model = Trip
    form_class = TripForm
    success_url = reverse_lazy('trips:list')

    def get_queryset(self):
        'get possible trips to update'
        return Trip.objects.for_user('change', self.request.user)
