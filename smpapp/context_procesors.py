import datetime
from .models import (
    SCHOOL_CLASS,
    Teacher,
    Student,
    SchoolSubject,
    StudentGrades,
)


def my_cp(request):
    cp_teachers = Teacher.objects.all()
    cp_students = Student.objects.all()
    cp_subjects = SchoolSubject.objects.all()
    cd_grades = StudentGrades.objects.all()
    ctx = {
        'date': datetime.date.today(),
        'version': '2.1.18.03.03',
        'cp_class': SCHOOL_CLASS,
        'cp_teachers': cp_teachers,
        'cp_students': cp_students,
        'cp_subjects': cp_subjects,
        'cd_grades': cd_grades,
    }
    return ctx
