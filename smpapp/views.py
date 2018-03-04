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


''' Student Section'''
class StudentView(View):
    def get(self, request, student_id):
        student = Student.objects.get(pk=student_id)
        subjects = SchoolSubject.objects.all()
        grades = StudentGrades.objects.filter(student_id=student_id)
        print(vars(student))
        ctx ={
            'student': student,
            'grades': grades,
            'subjects': subjects,
        }
        return render(request, 'student_full.html', ctx)


class Grades(View):

    def get(self, request, student_id, subject_id):
        student = Student.objects.get(pk=student_id)
        subject = SchoolSubject.objects.get(pk=subject_id)
        grades = StudentGrades.objects.filter(
            student_id=student_id,
            school_subject=subject_id
        )

        try:
            sum = 0
            for g in grades:
                sum += int(g.grade)
            avg = round(sum / len(grades), 2)
        except ZeroDivisionError:
            avg = 0

        ctx = {
            'student': student,
            'subject': subject,
            'grades': grades,
            'avg': avg,
        }
        return render(request, 'grades.html', ctx)


class StudentSearchView(View):

    def get(self, request):
        form = StudentSearchForm()
        return render(request, 'student_search.html', {'form': form})

    def post(self, request):
        form = StudentSearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            students = Student.objects.filter(last_name__icontains=name)
            # niezwaza na wielkosc znakow
            return render(request, 'student_search.html', {'form': form, 'students': students})