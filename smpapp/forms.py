from django import forms

from .models import (
    GRADES, Student, UnpreparedList,
)


''' Teacher Section '''

class StudentSearchForm(forms.Form):
    name = forms.CharField(label='Nazwisko ucznia')


class StudentGradesForm(forms.Form):
    grade = forms.ChoiceField(label='Ocena', choices=GRADES)


class PresenceListForm(forms.Form):

    student = forms.ModelChoiceField(label='Student', queryset=Student.objects.filter())
    day = forms.DateField(label='Data', widget=forms.HiddenInput())
    present = forms.NullBooleanField(label='Obecnosc')


class UnpreparedListForm(forms.ModelForm):
    class Meta:
        model = UnpreparedList
        fields = '__all__'


''' Auth Section '''

class LoginForm(forms.Form):
    login = forms.CharField(label='Login')
    password = forms.CharField(label='Haslo', widget=forms.PasswordInput)

