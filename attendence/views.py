from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Student, Teacher, Class
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import AddClass, TeacherForm
from django.contrib.auth import login, authenticate

def home(request):
    print(request.user)
    return render(request, 'attendence/home.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            usr = form.cleaned_data['username']
            new_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
        login(request, new_user)
        return redirect('teacher-form-page')
    else:
        form = UserCreationForm()

    context = {
        'form':form,
    }

    return render(request, 'attendence/register.html', context)

@login_required
def dashboard(request):
    teacher = Teacher.objects.filter(user=request.user)
    clss = Class.objects.filter(teacher=request.user.teacher)
    teacher = request.user.teacher
    context = {
        'teacher':teacher,
        'clss':clss,
    }
    return render(request, 'attendence/dashboard.html', context)

@login_required
def add_class(request):
    teacher = request.user.teacher
    if request.method == 'POST':
        form = AddClass(request.POST, initial={'teacher':teacher})
        if form.is_valid():
            form.save()
            return redirect('dashboard-page')
    else:
        form = AddClass(initial={'teacher':teacher})
    context = {
        'form':form,
    }
    return render(request, 'attendence/add_class.html', context)


@login_required
def attendence_sheet(request, brnch, sem, sec):
    students = Student.objects.filter(branch=brnch, sem=sem, sec=sec)
    print(students)
    context = {
        'students':students,
    }
    return render(request, 'attendence/attendence_sheet.html', context)

def teacher_form(request):
    user = request.user
    if request.method == 'POST':
        form = TeacherForm(request.POST, initial={'user':request.user.username})
        if form.is_valid():
            form.save()
        return redirect('dashboard-page')
    else:
        form = TeacherForm(initial={'user':user})

    context = {
        'form':form,
    }
    return render(request, 'attendence/teacher_form.html', context)

def counts(request):
    pass