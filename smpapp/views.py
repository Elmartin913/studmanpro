import datetime

from django.shortcuts import render
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseRedirect, request
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

from smpapp.models import (
    SCHOOL_CLASS,
    Student,
    SchoolSubject,
    StudentGrades,
    UnpreparedList,
    PresenceList,
    Book,
)

from smpapp.forms import (
    StudentSearchForm,
    StudentGradesForm,
    PresenceListForm,
    UnpreparedListForm,
    LoginForm,
    ChangePassForm,
    NewBookForm,
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
        presence_list = PresenceList.objects.filter(school_subject_id=subject_id,
                                                    day=datetime.date.today()
                                                    )

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
        date = datetime.date.today()
        studs = Student.objects.filter(school_class=class_id)
        form = PresenceListForm(initial={'day': date, 'student': studs})
        return render(request, 'class_presence.html', {'form': form})

    def post(self, request, class_id, subject_id, student_id):
        form = PresenceListForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            day = form.cleaned_data['day']
            present = form.cleaned_data['present']
            PresenceList.objects.create(
                student_id=student_id,
                day=day,
                present=present,
                school_subject_id=subject_id,
            )
            url = reverse_lazy('teacher_class', kwargs={
                'subject_id': subject_id,
                'class_id': class_id
            })
            return HttpResponseRedirect(url)


class UnpreparedListFormView(CreateView):
    form_class = UnpreparedListForm
    template_name = 'unprepared_form.html'
    success_url =reverse_lazy('teacher_search')



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



''' Auth Section '''

class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            login2 = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = authenticate(
                username=login2,
                password=password
            )
            if user is not None:
                login(request, user)
                return HttpResponse('Zalogowany {}'.format(user.username))
            else:
                return HttpResponse('Niepoprawne dane do logowania')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('login'))


class ChangePassView(View):

    def get(self, request, user_id):
        form = ChangePassForm()
        return render(request, 'change_pass.html', {'form': form})

    def post(self, request, user_id):
        form = ChangePassForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=user_id)
            user = authenticate(
                username=user.username,
                password=form.cleaned_data['old_pass']
            )
            if not user.check_password(form.cleaned_data['old_pass']):
                return HttpResponse('Niepoprane aktualne haslo')

            if form.cleaned_data['new_pass'] != form.cleaned_data['new_pass_2']:
                return HttpResponse('Nowe hasla nie s takie same')

            user.set_password(form.cleaned_data['new_pass'])
            user.save()
            return HttpResponse('Haso zmienione')


''' Library Section '''

class LibraryView(View):
    def get(self, request):
        return TemplateResponse(request, 'library.html')


class NewBookFormView(CreateView):
    form_class = NewBookForm
    template_name = 'book_create_form.html'
    success_url = reverse_lazy('library')


class BookUpdateView(UpdateView):
    model = Book
    template_name = 'book_update_form.html'
    fields = '__all__'
    success_url = reverse_lazy('library')


class BookDeleteView(DeleteView):
    model = Book
    template_name = 'book_form.html'
    success_url = reverse_lazy('library')


class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'


''' Auditorium Section '''