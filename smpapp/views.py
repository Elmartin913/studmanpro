from django.shortcuts import render
from django.http import request
from django.views import View
from django.template.response import TemplateResponse

from smpapp.models import (
    SCHOOL_CLASS,
    Student,
    SchoolSubject,
    StudentGrades,
    UnpreparedList,
    PresenceList,
)

# Create your views here.


# Landing Page
class LPView(View):
    def get(self, requset):
        return TemplateResponse (requset, 'index.html')

''' Teacher Section'''

# Full Teacher View
class TeacherStartView(View):
    def get(self, request):
        return render(request, 'teacher_base.html', {'all_class': SCHOOL_CLASS})


class TeacherView(View):
    def get(self, request, class_id, subject_id):
        students = Student.objects.filter(school_class=class_id)
        subject = SchoolSubject.objects.get(pk=subject_id)
        grades = StudentGrades.objects.filter(school_subject_id=subject_id)
        unprepared_list = UnpreparedList.objects.filter(school_subject_id=subject_id)
        presence_list = PresenceList.objects.filter(school_subject_id=subject_id)

        ctx = {
            'subject': subject,
            'students': students,
            'grades': grades,
            'unprepared_list': unprepared_list,
            'presence_list': presence_list,
            'class_id': class_id,
        }

        return render(request, 'teacher_full.html', ctx)




''' Student Section'''
class StudentView(View):
    def get(self, request, student_id):
        student = Student.objects.get(pk=student_id)
        grades = StudentGrades.objects.filter(student_id=student_id)
        unprepared_list = UnpreparedList.objects.filter(student_id=student_id)

        ctx ={
            'student': student,
            'grades': grades,
            'unprepared_list': unprepared_list,
        }
        return render(request, 'student_full.html', ctx)

