from django.shortcuts import render
from django.http import request
from django.views import View
from django.template.response import TemplateResponse

from smpapp.models import SCHOOL_CLASS, Student, SchoolSubject, StudentGrades

# Create your views here.


# Landing Page
class LPView(View):
    def get(self, requset):
        return TemplateResponse (requset, 'index.html')

''' Teacher Section'''

# Full Teacher View
class TeacherStartView(View):
    def get(self, request):
        return render(request, 'teacher_full.html', {'all_class': SCHOOL_CLASS})


class TeacherView(View):
    def get(self, request, class_id, subject_id):
        students = Student.objects.filter(school_class=class_id)
        subject = SchoolSubject.objects.get(pk=subject_id)
        grades = StudentGrades.objects.filter(school_subject_id=subject_id)

        ctx = {
            'all_class': SCHOOL_CLASS,
            'subject': subject,
            'students': students,
            'grades': grades,
        }

        return render(request, 'teacher_full.html', ctx)