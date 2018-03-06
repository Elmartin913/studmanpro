"""smp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from smpapp.views import (
    LPView,
    TeacherStartView, TeacherView, StudentSearchView,StudentGradesFormView,
    StudentView
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LPView.as_view(), name='lp'),
    # teacher
    path('teacher', TeacherStartView.as_view(), name='teacher_start'),
    path('teacher/search', StudentSearchView.as_view(), name='teacher_search'),
    path('teacher/<int:class_id>/<int:subject_id>', TeacherView.as_view(), name='teacher_class'),
    path('teacher/<int:class_id>/<int:subject_id>/<int:student_id>/grades', StudentGradesFormView.as_view(), name='teacher_edit_grades'),
    path('teacher/<int:class_id>/<int:subject_id>/<int:student_id>/unpr', TeacherView.as_view(), name='teacher_edit_unpr'),
    path('teacher/<int:class_id>/<int:subject_id>/pres', TeacherView.as_view(), name='teacher_edit_pres'),
    # studnent
    path('student/<int:student_id>', StudentView.as_view(), name='student_view'),
]
