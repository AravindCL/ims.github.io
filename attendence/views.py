from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Student, Teacher, Class, Count, Feedback, Item, Type, Subject, StudentMark
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import AddClass, TeacherForm, UserRegistrationForm, StudentForm, FeedbackForm
from django.contrib.auth import login, authenticate
from django.contrib import messages


def home(request):
    form = FeedbackForm()
    try:
        student = Student.objects.get(user=request.user)
        print(student.user)
        subjects = Subject.objects.filter(
            sem=student.sem, branch=student.branch)
    except:
        subjects = {}
        student = {}
    types = Type.objects.all()
    context = {
        'types': types,
        'subjects': subjects,
        'student': student,
    }

    return render(request, 'attendence/home.html', context)


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
        'form': form,
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
            messages.success(
                request, f'Your Response Has been successfully submitted, {request.user}')
        else:
            Feedback.objects.create(usr=None, name=name, message=message)
            messages.success(
                request, 'Your Response Has been successfully submitted')

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
        'teacher': teacher,
        'clss': clss,
    }
    return render(request, 'attendence/dashboard.html', context)


@login_required
def add_class(request):
    teacher = request.user.teacher

    if request.method == 'POST':
        form = AddClass(request.POST, initial={'teacher': teacher})
        branch = request.POST['branch']
        sem = request.POST['sem']
        sec = request.POST['sec']
        if branch == "" or sem == "" or sec == "":
            messages.warning(request, "Fill all the Fields")
        if form.is_valid():
            form.save()
            try:
                clss = Class.objects.get(
                    teacher=teacher, sem=sem, sec=sec, branch=branch)
                messages.success(request, 'Class Added Successfully')
            except:
                print('class already exits')
                messages.warning(request, 'Class Already Exists')
                todelet = Class.objects.filter(
                    teacher=teacher, sem=sem, sec=sec, branch=branch)[1]
                todelet.delete()
                return redirect('add-class-page')

            students = Student.objects.filter(sem=sem, branch=branch, sec=sec)
            for student in students:
                Count.objects.create(student=student, clss=clss, cnt=1)
                StudentMark.objects.create(student=student, clss=clss, marks1=0, marks2=0,marks3=0)
            return redirect('dashboard-page')
        form = AddClass(initial={'teacher': teacher})
        # return redirect('add-class-page')
    else:
        form = AddClass(initial={'teacher': teacher})
    context = {
        'form': form,
    }
    return render(request, 'attendence/add_class.html', context)


@login_required
def attendence_sheet(request, brnch, sem, sec):
    teachers = Teacher.objects.get(user=request.user)
    clss = Class.objects.get(teacher=teachers, branch=brnch, sem=sem, sec=sec)
    cnts = Count.objects.filter(clss=clss)
    students = Student.objects.filter(branch=brnch, sem=sem, sec=sec)
    for cnt in cnts:
        print(cnt.student.usn)

    # data = zip(students, cnts)
    # for i,j in data:
    #     print('----')
    #     print(i,j)

    context = {
        'students': students,
        'teacher': teachers,
        'cnts': cnts,
        # 'data':zip(students, cnts)
    }
    return render(request, 'attendence/attendence_sheet.html', context)


def studMarks(request, brnch, sem, sec):
    teachers = Teacher.objects.get(user=request.user)
    clss = Class.objects.get(teacher=teachers, branch=brnch, sem=sem, sec=sec)
    students = Student.objects.filter(branch=brnch, sem=sem, sec=sec)
    mrks = StudentMark.objects.filter(clss=clss)

    context = {
        'students': students,
        'teacher': teachers,
        'mrks': mrks,
        'clss': clss,
        # 'data':zip(students, cnts)
    }
    return render(request, 'attendence/markStudent.html', context)
# <str:username>/<int:sem>/<str:sec>/<str:branch>/<str:subject>/

def marksSub(request, sem, sec, branch, subject):
    print(sem, sec, subject, branch)
    print(request.GET)
    a = dict(request.GET)
    # b = list(request.GET).
    # print(b)
    print(a)
    arr1 = []
    arr2 = []
    count = 0
    for item,vals in a.items():
        if(count == 0):
            arr1 = vals
            count += 1
        else:
            arr2 = vals
    print(arr1, arr2)
    newarr = zip(arr1, arr2)
    clss = Class.objects.get(sem=sem, sec=sec, branch=branch, subject=subject)
    # for j in range(len(arr1)):
    count = 0
    while (count != len(arr1)):
        print("I am in for loop ...")
        mrks = StudentMark.objects.get(clss=clss, student__usn=arr1[count])
        print(arr1[count], arr1[count+1], arr1[count+2])
        mrks.marks1 = arr1[count+1]
        mrks.marks2 = arr1[count+2]
        mrks.marks3 = arr1[count+3]
        mrks.save()
        count += 4
        print("Saved ....")
        print(mrks)
    print("I am out of for loop")
    return redirect('marks-student-page', branch, sem, sec)

    exit()


def teacher_form(request):
    user = request.user
    if request.method == 'POST':
        password = request.POST['password']
        if password == 'sjcitteacher@21':
            form = TeacherForm(request.POST, initial={
                               'user': request.user.username})
        else:
            return redirect('teacher-form-page')
        if form.is_valid():
            form.save()
            return redirect('dashboard-page')
    else:
        form = TeacherForm(initial={'user': user})

    context = {
        'form': form,
    }
    return render(request, 'attendence/teacher_form.html', context)

# If you dont wanna go to hell, then better stay away from this function


def counts(request):
    print("------------------------")
    a = dict(request.GET)
    students = Student.objects.all()
    print('')
    print(request.GET)
    for i, j in a.items():
        sem = j[0].split()[2]
        sec = j[0].split()[3]
        branch = j[0].split()[4]
        students = Student.objects.filter(sem=sem, sec=sec, branch=branch)
        teacher = Teacher.objects.get(user=request.user)
        room = Class.objects.get(
            teacher=teacher, sem=sem, sec=sec, branch=branch)
        for i in j:
            print('------', i, '-------')
            print(j)
            for student in students:
                if i.split()[1] == student.usn:
                    try:
                        cnts = Count.objects.get(
                            student=student, clss=room).student
                    except:
                        cnts = None

                    if student == cnts:
                        prev = Count.objects.get(
                            student=student, clss=room).cnt
                        ct = Count.objects.get(student=student, clss=room)
                        ct.cnt = prev + 1
                        ct.save()
                        print('student is present')
                    else:
                        Count.objects.create(student=student, clss=room, cnt=1)

                        print('Student is absent')
                    break

        messages.success(request, "Attendence Taken succesfully")
        return redirect('dashboard-page')
    return redirect('dashboard-page')


def student_form(request):
    user = request.user
    print(user, "----")
    if request.method == 'POST':
        if request.POST['sem'] == "" or request.POST['sec'] == "" or request.POST['branch'] == "":
            messages.warning(request, 'All fields are required !!!')
            return redirect('student-form-page')
        clsses = Class.objects.filter(
            sem=request.POST['sem'], sec=request.POST['sec'], branch=request.POST['branch'])

        form = StudentForm(request.POST, initial={'user': request.user})
        # return redirect('student-form-page')
        if form.is_valid():
            form.save()
            student = Student.objects.get(usn=request.POST['usn'])
            for clss in clsses:
                Count.objects.create(student=student, clss=clss, cnt=1)
                StudentMark.objects.create(student=student, clss=clss, marks1=0, marks2=0, marks3=0)

            return redirect('home-page')
    else:
        form = StudentForm(initial={'user': user})

    context = {
        'form': form,
    }
    return render(request, 'attendence/student_form.html', context)


@login_required()
def rm_clss(request, brnch, sem, sec):
    teacher = request.user.teacher
    if request.method == 'POST':
        clss = Class.objects.get(
            teacher=teacher, branch=brnch, sem=sem, sec=sec)
        clss.delete()
        messages.success(request, 'Deleted Class Successfully ')
        return redirect('dashboard-page')
    context = {
        'branch': brnch,
        'sem': sem,
        'sec': sec
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
    clss = Class.objects.filter(
        sem=student.sem, sec=student.sec, branch=student.branch)
    cnts = Count.objects.filter(student=student)
    marks = StudentMark.objects.filter(student=student)
    context = {
        'cnts': cnts,
        'marks':marks,
    }
    return render(request, 'attendence/student_dashboard.html', context)


def idonno(request, type_):
    student = Student.objects.get(user=request.user)
    subjects = Subject.objects.filter(sem=student.sem, branch=student.branch)
    items = Item.objects.filter(tyPe__name=type_)
    context = {
        'items': items,
        'subjects': subjects,
        'type': type_,
    }
    return render(request, 'attendence/idonno.html', context)


def google_verification(request):

    return render(request, 'attendence/google645cd8e508c990d1.html')
