from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    branc = (
        ('cse','cse'),
        ('is', 'is'),
        ('civil', 'civil'),
        ('mechanical', 'mechanical'),
    )
    sem = (
        (1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),
    )
    section = (
        ('A','A'),('B','B'),('C','C'),('D','D'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    usn = models.CharField(max_length=200, null=True, blank=True, unique=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    branch = models.CharField(max_length = 200, choices=branc, null=True, blank=True)
    sem = models.IntegerField(choices=sem, null=True, blank=True)
    sec = models.CharField(max_length = 200, choices=section, null=True, blank=True)
    is_present = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return (self.usn + " " + self.name)



class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    branch = models.CharField(max_length=200, null=True, blank=True)
    your_favorite_quote = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Class(models.Model):
    branc = (
        ('cse','cse'),
        ('is', 'is'),
        ('civil', 'civil'),
        ('mechanical', 'mechanical'),
    )
    sem = (
        (1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),
    )
    section = (
        ('A','A'),('B','B'),('C','C'),('D','D'),
    )
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    branch = models.CharField(max_length = 200, choices=branc, null=True, blank=True)
    sem = models.IntegerField(choices=sem, null=True, blank=True)
    sec = models.CharField(max_length = 200, choices=section, null=True, blank=True)

    def __str__(self):
        return self.teacher.name + " " + str(self.sem) + self.sec

class Count(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    clss = models.ForeignKey(Class, on_delete=models.CASCADE, blank=True, null=True)
    cnt = models.IntegerField(null=True, blank=True)

    def __str__(self):
        # return (str(self.cnt))
        return str(self.cnt)