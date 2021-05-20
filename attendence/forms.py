from django.contrib.auth.forms import forms
from .models import Class, Teacher, Student, Feedback
from django.forms import ModelForm, Field
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Teacher

class AddClass(ModelForm):
    class Meta:
        model = Class 
        # fields = ['teacher', 'sem', 'sec', 'branch']
        fields = '__all__'

class TeacherForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Teacher
        fields = ['user', 'name', 'branch', 'your_favorite_quote', 'password']


class UserRegistrationForm(UserCreationForm):
    student = forms.BooleanField(required=False)
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'student']

class StudentForm(ModelForm):
    usn = forms.CharField(max_length=10, min_length=10,required=True)
    class Meta:
        model = Student
        fields = ['user', 'usn', 'name', 'branch', 'sem', 'sec']


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'message']