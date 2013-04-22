'forms for Trips'
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from django import forms

from .models import Trip

TRIP_THEMES = {
    'editor': 'epic-light.css',
    'preview': 'github.css',
}

class TripForm(forms.ModelForm):
    'Form for a trip'
    class Meta:
        model = Trip
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        'initialize this form'
        # Initialize crispy form helper
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Details about your trip',
                'where', 'when', 'letter', 'video',
            ),
            Fieldset(
                'Funding Details',
                'money_explanation', 'due', 'amount_needed',
            ),
            FormActions(
                Submit('submit', 'Submit', css_class='button'),
            )
        )
        self.user = kwargs.pop('user', None)
        super(TripForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        'save with user'
        orig_commit, kwargs['commit'] = kwargs.get('commit', True), False
        instance = super(TripForm, self).save(*args, **kwargs)
        create = instance.pk is None

        if create:
            instance.user = self.user

        if orig_commit:
            instance.save()

        if create and orig_commit:
            instance.fully_authorize(self.user)

        return instance
