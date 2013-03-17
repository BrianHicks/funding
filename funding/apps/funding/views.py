'views for funding'
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView
from guardian.shortcuts import assign, get_objects_for_user

from funding.apps.funding.forms import BalancedAccountForm
from funding.apps.funding.models import BalancedAccount, BalancedAccountTypes
from funding.common.views import LoginRequiredMixin


class BalancedAccountAddView(LoginRequiredMixin, CreateView):
    'view to display the add account form to the receiver'
    form_class = BalancedAccountForm
    template_name = 'funding/funding/receiver_account_add.html'
    success_url = reverse_lazy('funding:list')

    def get_form_kwargs(self):
        'get keyword arguments to build form'
        form_kwargs = super(BalancedAccountAddView, self).get_form_kwargs()
        data = form_kwargs.get('data', {})
        data['kind'] = BalancedAccountTypes.BANK_ACCOUNT
        return form_kwargs

    def form_valid(self, *args, **kwargs):
        'associate user with auth if form is valid'
        response = super(BalancedAccountAddView, self).form_valid(*args, **kwargs)

        # associate logged-in user with BalancedAccount
        self.object.fully_authorize(self.request.user)

        return response


class BalancedAccountListView(LoginRequiredMixin, ListView):
    'view to list funding sources'
    model = BalancedAccount

    def get_queryset(self):
        'get a queryset for the user'
        return get_objects_for_user(
            self.request.user, 'funding.view_balancedaccount'
        )


class BalancedAccountDeleteView(LoginRequiredMixin, DeleteView):
    'view to delete funding sources'
    model = BalancedAccount
    success_url = reverse_lazy('funding:list')

    def get_queryset(self):
        'get queryset for BalancedAccounts'
        return get_objects_for_user(
            self.request.user, 'funding.delete_balancedaccount',
        )
