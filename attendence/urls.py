from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home-page'),
    path('register/', views.register, name='register-page'),
    path('dashboard/', views.dashboard, name='dashboard-page'),
    path('count-attdnce/', views.counts, name='count-attdnce-page'),
    path('add-class/', views.add_class, name='add-class-page'),
    path('student-form/', views.student_form, name='student-form-page'),
    path('attendence/<str:brnch>/<int:sem>/<str:sec>/', views.attendence_sheet, name='attendence-page'),
    path('teacher-form/', views.teacher_form, name='teacher-form-page'),
    path('login/', auth_views.LoginView.as_view(template_name='attendence/login.html') , name='login-page'),
    path('logout/',auth_views.LogoutView.as_view(template_name='attendence/logout.html'),name='logout-page'),
]