'views for funding'
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from guardian.shortcuts import assign, get_objects_for_user

from funding.apps.funding.forms import BankAccountForm
from funding.apps.funding.models import BankAccount
from funding.common.views import LoginRequiredMixin


class BankAccountAddView(LoginRequiredMixin, CreateView):
    'view to display the add account form to the receiver'
    form_class = BankAccountForm
    template_name = 'funding/funding/receiver_account_add.html'
    success_url = reverse_lazy('funding:list')

    def form_valid(self, *args, **kwargs):
        response = super(BankAccountAddView, self).form_valid(*args, **kwargs)

        # associate logged-in user with BankAccount
        assign('view_bankaccount', self.request.user, self.object)
        assign('change_bankaccount', self.request.user, self.object)
        assign('delete_bankaccount', self.request.user, self.object)

        return response


class BankAccountListView(LoginRequiredMixin, ListView):
    'view to list funding sources'
    model = BankAccount

    def get_queryset(self):
        'get a queryset for the user'
        return get_objects_for_user(
            self.request.user, 'funding.view_bankaccount'
        )
