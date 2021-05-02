from django.contrib.auth.forms import forms
from .models import Class, Teacher
from django.forms import ModelForm

class AddClass(ModelForm):
    class Meta:
        model = Class 
        fields = '__all__'

class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'