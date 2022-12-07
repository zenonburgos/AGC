from django.forms import *


class ReportForm(Form):

    date_range = CharField(widget=TextInput(attrs={
        'class': 'form-control flatpickr flatpickr-input active',
        'id': 'rangeCalendarFlatpickr',
        'autocomplete': 'off',
    }))