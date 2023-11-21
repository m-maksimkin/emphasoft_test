from .models import Booking

from django import forms


ORDERING_CHOICES = (('price', 'цена'), ('capacity', 'вместимость'))


class SortRoomsForm(forms.Form):
    ordering = forms.ChoiceField(choices=ORDERING_CHOICES, required=False,
                                 label='сорт')
    start_date = forms.DateField(required=False, label='дата начала')
    stop_date = forms.DateField(required=False, label='дата окончания')


class BookingCreateForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('start_date', 'end_date')

