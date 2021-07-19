from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    branc = (
        ('CSE', 'CSE'),
        ('ISE', 'ISE'),
        ('Civil', 'Civil'),
        ('ME', 'ME'),
        ('Aeronautical', 'Aeronautical'),
        ('ECE', 'ECE'),
        ('Aerospace', 'Aerospace'),
    )
    sem = (
        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8),
    )
    section = (
        ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    usn = models.CharField(max_length=10, null=True, unique=True)
    name = models.CharField(max_length=200, null=True)
    branch = models.CharField(max_length=200, choices=branc, null=True)
    sem = models.IntegerField(choices=sem, null=True)
    sec = models.CharField(max_length=200, choices=section, null=True)

    def __str__(self):
        return (str(self.usn) + " " + str(self.name) + " " + str(self.sem))


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    department = models.CharField(max_length=200, null=True, blank=True)
    your_favorite_quote = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.name)


class Class(models.Model):
    branc = (
        ('CSE', 'CSE'),
        ('ISE', 'ISE'),
        ('Civil', 'Civil'),
        ('ME', 'ME'),
        ('Aeronautical', 'Aeronautical'),
        ('ECE', 'ECE'),
        ('Aerospace', 'Aerospace'),
    )
    sem = (
        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8),
    )
    section = (
        ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'),
    )
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    branch = models.CharField(
        max_length=200, choices=branc, null=True, blank=False)
    sem = models.IntegerField(choices=sem, null=True, blank=False)
    sec = models.CharField(
        max_length=200, choices=section, null=True, blank=False)
    subject = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.teacher.name + " " + str(self.sem) + self.sec


class Count(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, null=True, blank=False)
    clss = models.ForeignKey(
        Class, on_delete=models.CASCADE, blank=False, null=True)
    cnt = models.IntegerField(null=True, blank=False)

    def __str__(self):
        # return (str(self.cnt))
        return str(self.cnt)


class Feedback(models.Model):
    usr = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    message = models.TextField()

    def __str__(self):
        return self.name


class Type(models.Model):
    image_url = models.CharField(max_length=800, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Subject(models.Model):
    branc = (
        ('CSE', 'CSE'),
        ('ISE', 'ISE'),
        ('Civil', 'Civil'),
        ('ME', 'ME'),
        ('Aeronautical', 'Aeronautical'),
        ('ECE', 'ECE'),
        ('Aerospace', 'Aerospace'),
    )
    sem = (
        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8),
    )

    sub = models.CharField(max_length=200, null=True, blank=True)
    sem = models.IntegerField(choices=sem, blank=True, null=True)
    branch = models.CharField(
        choices=branc, blank=True, null=True, max_length=200)

    def __str__(self):
        return f'{self.sub} sem:{self.sem} branch:{self.branch}'


class Item(models.Model):
    sub = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    tyPe = models.ForeignKey(Type, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True, blank=True)
    ques_description = models.CharField(max_length=200, null=True, blank=True)
    document_ques = models.FileField(
        upload_to='tutorials/', null=True, blank=True)
    ans_description = models.CharField(max_length=200, null=True, blank=True)
    document_ans = models.FileField(
        upload_to='tutorials/', null=True, blank=True)

    def __str__(self):
        return self.ques_description


class StudentMark(models.Model):
    examType = (
        ('IA-1', 'IA-1'),
        ('IA-2', 'IA-2'),
        ('IA-3', 'IA-3'),

    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    clss = models.ForeignKey(Class, on_delete=models.CASCADE, blank=False, null=True)
    exmtype = models.CharField(choices=examType, blank=True, null=True, max_length=200)
    marks1 = models.IntegerField(null=True, blank=False)
    marks2 = models.IntegerField(null=True, blank=False)
    marks3 = models.IntegerField(null=True, blank=False)

    def __str__(self):
        return self.student.name + str(self.clss) + " " + str(self.marks1)


# class Tutorial(models.Model):
#     branc = (
#         ('CSE','CSE'),
#         ('ISE', 'ISE'),
#         ('Civil', 'Civil'),
#         ('ME', 'ME'),
#         ('Aeronautical', 'Aeronautical'),
#         ('ECE', 'ECE'),
#         ('Aerospace', 'Aerospace'),
#     )
#     sem = (
#         (1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),
#     )

#     sub = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
#     title = models.CharField(max_length=200, null=True, blank=True)
#     ques_description = models.CharField(max_length=200, null=True, blank=True)
#     document = models.FileField(upload_to='tutorials/', null=True, blank=True)
#     ans_description = models.CharField(max_length=200, null=True, blank=True)
#     document = models.FileField(upload_to='tutorials/', null=True, blank=True)

#     def __str__(self):
#         return self.title


# class QuestionPaper(models.Model):
#     sub = models.ForeignKey(Subject, on_delete=models.CASCADE)
#     title = models.CharField(max_length=200, null=True, blank=True)
#     ques_description = models.CharField(max_length=200, null=True, blank=True)
#     document = models.FileField(upload_to='tutorials/', null=True, blank=True)
#     ans_description = models.CharField(max_length=200, null=True, blank=True)
#     document = models.FileField(upload_to='tutorials/', null=True, blank=True)


#     def __str__(self):
#         return self.title

# class Note(models.Model):
#     sub = models.ForeignKey(Subject, on_delete=models.CASCADE)
#     title = models.CharField(max_length=200, null=True, blank=True)
#     ques_description = models.CharField(max_length=200, null=True, blank=True)
#     document = models.FileField(upload_to='tutorials/', null=True, blank=True)
#     ans_description = models.CharField(max_length=200, null=True, blank=True)
#     document = models.FileField(upload_to='tutorials/', null=True, blank=True)


#     def __str__(self):
#         return self.title


# class ImportantQuestions(models.Model):
#     sub = models.ForeignKey(Subject, on_delete=models.CASCADE)
#     title = models.CharField(max_length=200, null=True, blank=True)
#     ques = models.CharField(max_length=200, null=True, blank=True)
#     ans = models.CharField(max_length=200, null=True, blank=True)

#     def __str__(self):
#         return self.title
