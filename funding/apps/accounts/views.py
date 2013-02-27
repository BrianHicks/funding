'views for accounts'
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from funding.apps.accounts.forms import BankAccountForm
from funding.apps.accounts.models import BankAccount
from funding.common.views import LoginRequiredMixin


class ReceiverAddAccountView(LoginRequiredMixin, CreateView):
    'view to display the add account form to the receiver'
    form_class = BankAccountForm
    template_name = 'accounts/funding/receiver_account_add.html'
    success_url = reverse_lazy('funding:list')


class FundingListView(LoginRequiredMixin, ListView):
    'view to list funding sources'
    model = BankAccount
