import datetime

from django.shortcuts import render
from django.views import View
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseRedirect, request
from django.urls import reverse, reverse_lazy

from smpapp.models import (
    SCHOOL_CLASS,
    Student,
    SchoolSubject,
    StudentGrades,
    UnpreparedList,
    PresenceList,
)

from smpapp.forms import (
    StudentSearchForm,
    StudentGradesForm,
    PresenceListForm,
    UnpreparedListForm,
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


class StudentSearchView(View):

    def get(self, request):
        form = StudentSearchForm()
        return render(request, 'student_search.html', {'form': form})

    def post(self, request):
        form = StudentSearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            students = Student.objects.filter(last_name__icontains=name)
            return render(request, 'student_search.html', {'form': form, 'students': students})


class StudentGradesFormView(View):
    def get(self, request, class_id, subject_id, student_id):
        form = StudentGradesForm()
        grades = StudentGrades.objects.filter(
            student_id=student_id,
            school_subject=subject_id
        )
        print(vars(grades))
        ctx = {
            'grades': grades,
            'form': form,
        }
        return render(request, 'teacher_grades.html', ctx)

    def post(self, request, class_id, subject_id, student_id):
        form = StudentGradesForm(request.POST)
        if form.is_valid():
            grade = form.cleaned_data['grade']
            grades = StudentGrades.objects.filter(
                student_id=student_id,
                school_subject=subject_id
            )

            try:
                sum = float(grade)
                for g in grades:
                    sum += int(g.grade)
                avg = round(sum / (len(grades)+1), 2)
            except ZeroDivisionError:
                avg = 0

            grades = StudentGrades.objects.create(
                school_subject_id=subject_id,
                student_id=student_id,
                grade = float(grade),
                avg = avg,
            )

            url = reverse('teacher_class', kwargs={
                'class_id': class_id,
                'subject_id': subject_id,
            })
            return HttpResponseRedirect(url)


class PresenceListFormView(View):

    def get(self, request, class_id, subject_id, student_id):
        day = datetime.date.today()
        form = PresenceListForm(initial={'day': day})
        return render(request, 'class_presence.html', {'form': form})

    def post(self, request, class_id, subject_id):
        form = PresenceListForm(request.POST)
        day = datetime.date.today()
        if form.is_valid():
            student = form.cleaned_data['student']
            day = form.cleaned_data['day']
            present = form.cleaned_data['present']
            PresenceList.objects.create(
                student=student,
                day=day,
                present=present
            )
            url = reverse('teacher_class', kwargs={
                'class_id': class_id,
                'subject_id': subject_id,
            })
            return HttpResponseRedirect(url)



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

