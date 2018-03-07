from django import forms

from .models import (
    GRADES, Student, PresenceList, UnpreparedList, StudentGrades
)

class StudentSearchForm(forms.Form):
    name = forms.CharField(label='Nazwisko ucznia')


class StudentGradesForm(forms.Form):
    grade = forms.ChoiceField(label='Ocena', choices=GRADES)


class PresenceListForm(forms.Form):

    student = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,label="Students")
    day = forms.DateField(label='Data', widget=forms.HiddenInput())
    present = forms.NullBooleanField(label='Obecny? ')



class UnpreparedListForm(forms.ModelForm):
    class Meta:
        model = UnpreparedList
        fields = '__all__'


