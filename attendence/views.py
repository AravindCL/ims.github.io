from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Student, Teacher, Class, Count, Feedback
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import AddClass, TeacherForm, UserRegistrationForm, StudentForm, FeedbackForm
from django.contrib.auth import login, authenticate
from django.contrib import messages

def home(request):
    print(request.user)
    form = FeedbackForm()
    
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

def feedback(request):
    if request.method == 'POST':
        user = request.user
        print(user)
        name = request.POST['name']
        message = request.POST['message']
        if user in User.objects.all():
            Feedback.objects.create(usr=user, name=name, message=message)
            messages.success(request, f'Your Response Has been successfully submitted, {request.user}')
        else:
            Feedback.objects.create(usr=None, name=name, message=message)
            messages.success(request, 'Your Response Has been successfully submitted')


    return redirect('home-page')

@login_required
def dashboard(request):
    try:
        teacher = Teacher.objects.filter(user=request.user)
        clss = Class.objects.filter(teacher=request.user.teacher)
    except:
        return redirect('student-dashboard-page')

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
        branch = request.POST['branch']
        sem = request.POST['sem']
        sec = request.POST['sec']
        if branch == "" or sem == "" or sec == "":
            messages.warning(request, "Fill all the Fields")
        if form.is_valid():
            form.save()
            try:
                clss = Class.objects.get(teacher=teacher, sem=sem, sec=sec, branch=branch)
                messages.success(request, 'Class Added Successfully')
            except:
                print('class already exits')
                messages.warning(request, 'Class Already Exists')
                todelet = Class.objects.filter(teacher=teacher, sem=sem, sec=sec, branch=branch)[1]
                todelet.delete()
                return redirect('add-class-page')
            
            students = Student.objects.filter(sem=sem, branch=branch, sec=sec)
            for student in students:
                Count.objects.create(student=student, clss=clss, cnt=1)
            return redirect('dashboard-page')
        form = AddClass(initial={'teacher':teacher})
        # return redirect('add-class-page')
    else:
        form = AddClass(initial={'teacher':teacher})
    context = {
        'form':form,
    }
    return render(request, 'attendence/add_class.html', context)


@login_required
def attendence_sheet(request, brnch, sem, sec):
    teachers = Teacher.objects.get(user=request.user)
    clss = Class.objects.get(teacher=teachers,branch=brnch, sem=sem, sec=sec)
    cnts = Count.objects.filter(clss=clss)
    students = Student.objects.filter(branch=brnch, sem=sem, sec=sec)
    for cnt in cnts:
        print(cnt.student.usn)
        
    data = zip(students, cnts)
    for i,j in data:
        print('----')
        print(i,j)
    
    context = {
        'students':students,
        'teacher':teachers,
        'cnts':cnts,
        'data':zip(students, cnts)
    }
    return render(request, 'attendence/attendence_sheet.html', context)

def teacher_form(request):
    user = request.user
    if request.method == 'POST':
        password = request.POST['password']
        if password == 'sjcitteacher@21':
            form = TeacherForm(request.POST, initial={'user':request.user.username})
        else:
            return redirect('teacher-form-page')
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
    a = dict(request.GET)
    students = Student.objects.all()
    print('')
    print(request.GET)
    for i,j in a.items():
        sem = j[0].split()[2]
        sec = j[0].split()[3]
        branch = j[0].split()[4]
        students = Student.objects.filter(sem=sem, sec=sec, branch=branch)
        teacher = Teacher.objects.get(user=request.user)
        room = Class.objects.get(teacher=teacher,sem=sem, sec=sec, branch=branch)
        for i in j:
            print('------',i,'-------')
            print(j)
            for student in students:
                if i.split()[1] == student.usn:
                    try:
                        cnts = Count.objects.get(student=student, clss=room).student
                    except:
                        cnts = None
     
                    if student == cnts:
                        prev = Count.objects.get(student=student, clss=room).cnt
                        ct = Count.objects.get(student=student, clss=room)
                        ct.cnt = prev + 1
                        ct.save()
                        print('student is present')
                    else:
                        Count.objects.create(student=student, clss=room ,cnt=1)

                        print('Student is absent')
                    break
                    
        messages.success(request, "Attendence Taken succesfully")   
        return redirect('dashboard-page')
    return redirect('dashboard-page')


def student_form(request):
    user = request.user
    print(user,"----")
    if request.method == 'POST':
        if request.POST['sem'] == "" or request.POST['sec'] == "" or request.POST['branch'] == "":
            messages.warning(request, 'All fields are required !!!')
            return redirect('student-form-page')
        clsses = Class.objects.filter(sem=request.POST['sem'], sec=request.POST['sec'], branch=request.POST['branch'])
       
        form = StudentForm(request.POST, initial={'user':request.user})
            # return redirect('student-form-page')
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

@login_required()
def rm_clss(request, brnch, sem, sec):
    teacher = request.user.teacher
    if request.method == 'POST':
        clss = Class.objects.get(teacher=teacher, branch=brnch, sem=sem, sec=sec)
        clss.delete()
        messages.success(request, 'Deleted Class Successfully ')
        return redirect('dashboard-page')
    context = {
        'branch':brnch,
        'sem':sem,
        'sec':sec
    }
    return render(request, 'attendence/confirm_rm_clss.html', context)


def check_user_registered(request):
    user = request.user
    try:
        Student.objects.get(user=user)
        print('Found ....')
        return redirect('student-dashboard-page')
    except:
        try:
            Teacher.objects.get(user=user)
            return redirect('dashboard-page')
        except:
            return redirect('student-form-page')


def student_dashboard(request):
    student = Student.objects.get(user=request.user)
    print(request.user, student)
    clss = Class.objects.filter(sem=student.sem, sec=student.sec, branch=student.branch)
    for j in clss:
        print(j)
    cnts = Count.objects.filter(student=student)
    for i in cnts:
        print(i.clss)
    context = {
        'cnts':cnts,
    }
    return render(request, 'attendence/student_dashboard.html', context)