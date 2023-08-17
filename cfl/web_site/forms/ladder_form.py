from django import forms

from web_site.models import Ladder


class DateInput(forms.DateInput):
    input_type = 'date'


class AddLadderForm(forms.ModelForm):
    end_date = forms.DateField(widget=DateInput(format='%Y-%m-%d', attrs={'class': 'form-control'}), required=False,
                               label='End date')

    class Meta:
        model = Ladder
        fields = ['name', 'rules', 'end_date']
