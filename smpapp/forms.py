from django import forms


class StudentSearchForm(forms.Form):

    name = forms.CharField(label='Nazwisko ucznia')