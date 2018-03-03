from django.contrib import admin

from .models import Student, Teacher, SchoolSubject

# Register your models here.

def suspend(admin, request, queryset):
    queryset.update(active=True)

suspend.short_description = 'Zawieś'


def unsuspend(admin, request, queryset):
    queryset.update(active=False)

unsuspend.short_description = 'Aktywój'

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'school_class', 'active']
    actions = (suspend, unsuspend)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'active']
    actions = (suspend, unsuspend)


@admin.register(SchoolSubject)
class SchoolSubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'teacher_list']

    def teacher_list(self, obj):
        return ', '.join([str(t) for t in obj.teacher.all()])