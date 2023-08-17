from django import forms


class InviteForm(forms.Form):
    username = forms.CharField(label='Username', max_length=120, min_length=5)
