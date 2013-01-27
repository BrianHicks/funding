'views for accounts'
from django.views.generic.edit import FormView

from funding.apps.accounts.forms import ReceiverAddAccountForm
from funding.common.views import LoginRequiredMixin


class ReceiverAddAccountView(LoginRequiredMixin, FormView):
    'view to display the add account form to the receiver'
    form_class = ReceiverAddAccountForm
    template_name = 'accounts/funding/receiver_account_add.html'
