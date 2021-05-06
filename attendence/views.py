from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Student, Teacher, Class, Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import AddClass, TeacherForm, UserRegistrationForm, StudentForm
from django.contrib.auth import login, authenticate

def home(request):
    print(request.user)
    return render(request, 'attendence/home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            usr = form.cleaned_data['username']
            new_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            print(form.cleaned_data['username'])
        print(form.cleaned_data['password1'])
        login(request, new_user)
        try:
            request.POST['student']
            return redirect('student-form-page')
        except:
            return redirect('teacher-form-page')
    else:
        form = UserRegistrationForm()

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
    teacher = Teacher.objects.get(user=request.user)
    # clss = Class.objects.get()
    
    students = Student.objects.filter(branch=brnch, sem=sem, sec=sec)    
    context = {
        'students':students,
        'teacher':teacher,
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
    print("------------------------")
    students = Student.objects.all()

    a = dict(request.GET)
    print('')
    print(request.GET)
    for i,j in a.items():
        sem = j[0].split()[2]
        sec = j[0].split()[3]
        # student = j[0].split()[4]
        teacher = Teacher.objects.get(user=request.user)
        room = Class.objects.get(teacher=teacher,sem=sem, sec=sec)
        for i in j:
            # print(i)
            for student in students:
                if i.split()[1] == student.usn:
                    try:
                        cnts = Count.objects.get(student=student, clss=room).student
                    except:
                        cnts = None
                    print(cnts)
                    # for cn in cnts:
                    #     # Count.objects.update(student=)
                    #     print(student)
                    #     print('$$$$')
                    #     print(cnts)
                    #     print(cn)
                    #     print('*****')
                    print(student)
                    if student == cnts:
                        prev = Count.objects.get(student=student, clss=room).cnt
                        ct = Count.objects.get(student=student, clss=room)
                        ct.cnt = prev + 1
                        ct.save()
                        print('student is present')
                    else:
                        Count.objects.create(student=student, clss=room ,cnt=22)

                        print('Student is absent')

        return redirect('dashboard-page')
    print('------------------------')
    return redirect('dashboard-page')


def student_form(request):
    user = request.user
    if request.method == 'POST':
        form = StudentForm(request.POST, initial={'user':request.user.username})
        if form.is_valid():
            form.save()
        return redirect('home-page')
    else:
        form = StudentForm(initial={'user':user})

    context = {
        'form':form,
    }
    return render(request, 'attendence/student_form.html', context)