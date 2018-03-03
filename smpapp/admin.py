from django.contrib import admin

from .models import Student, Teacher, SchoolSubject, Author, Book, Tag
# Register your models here.

''' ------------------- SCHOOL SECTION ------------------- '''

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


''' ------------------- LIBRARY SECTION ------------------- '''

def rented(admin, request, queryset):
    queryset.update(is_borrowed=True)

rented.short_description = 'Wypożyczona'


def returned(admin, request, queryset):
    queryset.update(is_borrowed=False)

returned.short_description = 'Zwrócona'

class BookTagInLineAdmin(admin.TabularInline):
    model = Book.tags.through

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'gender', 'author', 'is_borrowed', 'tags_list']
    inlines = (BookTagInLineAdmin,)
    actions = (rented, returned)

    def tags_list(self, obj):
        return ', '.join([str(t) for t in obj.tags.all()])


