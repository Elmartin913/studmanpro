from django.db import models

# Create your models here.

''' ------------------- SCHOOL SECTION ------------------- '''

SCHOOL_CLASS = (
    (1, "1 klasa"),
    (2, "2 klasa"),
    (3, "3 klasa"),
)

GRADES = (
    (1, "1"),
    (1.5, "1+"),
    (1.75, "2-"),
    (2, "2"),
    (2.5, "2+"),
    (2.75, "3-"),
    (3, "3"),
    (3.5, "3+"),
    (3.75, "4-"),
    (4, "4"),
    (4.5, "4+"),
    (4.75, "5-"),
    (5, "5"),
    (5.5, "5+"),
    (5.75, "6-"),
    (6, "6")
)



class Student(models.Model):
    first_name = models.CharField(max_length=64, verbose_name='Imię')
    last_name = models.CharField(max_length=64, verbose_name='Nazwisko')
    school_class = models.IntegerField(choices=SCHOOL_CLASS, verbose_name='Klasa')
    email = models.EmailField(verbose_name='Email', blank=True)
    suspended = models.BooleanField(default=True, verbose_name='Aktywny')
    add_date = models.DateField(auto_now_add=True)
    # relationships: SchoolSubject, StudentGrades, UnpreparedList
    #actions:
    active = models.BooleanField(default=True, verbose_name='Aktywny')

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Studenci'

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)



class Teacher(models.Model):
    first_name = models.CharField(max_length=64, verbose_name='Imię')
    last_name = models.CharField(max_length=64, verbose_name='Nazwisko')
    email = models.EmailField(verbose_name='Email', blank=True)
    suspended = models.BooleanField(default=True, verbose_name='Aktywny')
    add_date = models.DateField(auto_now_add=True)
    # relationships: school_subject
    #actions:
    active = models.BooleanField(default=True, verbose_name='Aktywny')

    class Meta:
        verbose_name = 'Nauczyciel'
        verbose_name_plural = 'Nauczyciele'

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)



class SchoolSubject(models.Model):
    name = models.CharField(max_length=64, verbose_name='Przedmiot')
    # relationships: teacher
    teacher = models.ManyToManyField(Teacher)

    class Meta:
        verbose_name = 'Przedmiot'
        verbose_name_plural = 'Przedmioty'


    def __str__(self):
        return self.name



class StudentGrades(models.Model):
    grade = models.FloatField(choices=GRADES)
    # relationships:
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    school_subject = models.ForeignKey(SchoolSubject, on_delete=models.CASCADE)


class PresenceList(models.Model):
    day = models.DateField()
    present = models.NullBooleanField()
    # relationships:
    student = models.ForeignKey(Student, on_delete=models.CASCADE)


class UnpreparedList(models.Model):
    day = models.DateField()
    # relationships:
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    school_subject = models.ForeignKey(SchoolSubject,on_delete=models.CASCADE)


''' ------------------- LIBRARY SECTION ------------------- '''

GENRES = (
    (1, 'podręczniki'),
    (2, 'prace naukowe'),
    (3, 'magazyny naukowe'),
    (4, 'ćwiczenia'),
    (5, 'vademecum'),
)

class Author(models.Model):
    first_name = models.CharField(max_length=256, verbose_name='Imie')
    last_name = models.CharField(max_length=256, verbose_name='Nazwisko')

    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autorzy'

    @property
    def name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=256, verbose_name='Tytul')
    gender = models.IntegerField(choices=GENRES, verbose_name='Gatunek')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    is_borrowed = models.NullBooleanField(default=False)
    date_added = models.DateField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', related_name='books') # 'Tag' bo klasa tag jest nizej

    class Meta:
        verbose_name = 'Książka'
        verbose_name_plural = 'Książki'

    def __str__(self):
        return self.title


class Tag(models.Model):
    tag_name = models.CharField(null = True, max_length=256, verbose_name='Tag')
    #books
    def __str__(self):
        return self.tag_name

    @property
    def books_string(self):
        titles = [book.title for book in self.books.all()]
        return ', '.join(titles)


