from django import forms

from .models import (
    Student, PresenceList, UnpreparedList, StudentGrades
)

class StudentSearchForm(forms.Form):
    name = forms.CharField(label='Nazwisko ucznia')


class StudentGradesForm(forms.Form):
    grade = forms.ChoiceField(label='Ocena', choices=SCHOOL_CLASS)


class PresenceListForm(forms.Form):

    student = forms.ModelChoiceField(label='Student', queryset=Student.objects.all())
    day = forms.DateField(label='Data', widget=forms.HiddenInput())
    present = forms.NullBooleanField(label='ObecnyS')


class UnpreparedListForm(forms.ModelForm):
    class Meta:
        model = UnpreparedList
        excude = ['school_subject', ]


