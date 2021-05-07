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
        tch = request.POST['teacher']
        print('----', tch, '---')
        branch = request.POST['branch']
        sem = request.POST['sem']
        sec = request.POST['sec']
        students = Student.objects.filter(sem=sem, branch=branch, sec=sec)
        form = AddClass(request.POST, initial={'teacher':teacher})
        
        if form.is_valid():
            form.save()
            clss = Class.objects.get(teacher=teacher, sem=sem, sec=sec, branch=branch)
            for student in students:
                Count.objects.create(student=student, clss=clss, cnt=1)
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
    clss = Class.objects.get(teacher=teacher,branch=brnch, sem=sem, sec=sec)
    cnts = Count.objects.filter(clss=clss)
    students = Student.objects.filter(branch=brnch, sem=sem, sec=sec)
    data = zip(students, cnts)
    for i,j in data:
        print('----')
        print(i,j)
    
    context = {
        'students':students,
        'teacher':teacher,
        'cnts':cnts,
        'data':zip(students, cnts)
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

# If you dont wanna go to hell, then better stay away from this function
def counts(request):
    print("------------------------")
    students = Student.objects.all()

    a = dict(request.GET)
    print('')
    print(request.GET)
    for i,j in a.items():
        sem = j[0].split()[2]
        sec = j[0].split()[3]
        teacher = Teacher.objects.get(user=request.user)
        room = Class.objects.get(teacher=teacher,sem=sem, sec=sec)
        for i in j:
            for student in students:
                if i.split()[1] == student.usn:
                    try:
                        cnts = Count.objects.get(student=student, clss=room).student
                    except:
                        cnts = None
                    print(cnts)
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
    print(user,"----")
    if request.method == 'POST':
        form = StudentForm(request.POST, initial={'user':request.user})
        clsses = Class.objects.filter(sem=request.POST['sem'], sec=request.POST['sec'], branch=request.POST['branch'])
        if form.is_valid():
            form.save()
            student = Student.objects.get(usn=request.POST['usn'])
            for clss in clsses:
                Count.objects.create(student=student, clss=clss, cnt=1)

        return redirect('home-page')
    else:
        form = StudentForm(initial={'user':user})

    context = {
        'form':form,
    }
    return render(request, 'attendence/student_form.html', context)