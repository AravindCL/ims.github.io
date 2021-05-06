from django.contrib.auth.forms import forms
from .models import Class, Teacher, Student
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class AddClass(ModelForm):
    class Meta:
        model = Class 
        fields = '__all__'

class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'

class UserRegistrationForm(UserCreationForm):
    student = forms.BooleanField(required=False)
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'student']

class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'