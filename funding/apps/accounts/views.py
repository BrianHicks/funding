'views for accounts'
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from funding.apps.accounts.forms import BankAccountForm
from funding.common.views import LoginRequiredMixin


class ReceiverAddAccountView(LoginRequiredMixin, FormView):
    'view to display the add account form to the receiver'
    form_class = BankAccountForm
    template_name = 'accounts/funding/receiver_account_add.html'
    success_url = reverse_lazy('funding:index')

class FundingListView(LoginRequiredMixin, ListView):
    'view to list funding sources'
