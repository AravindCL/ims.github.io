from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home-page'),
    path('register/', views.register, name='register-page'),
    path('dashboard/', views.dashboard, name='dashboard-page'),
    path('dashboard_student/', views.student_dashboard,name='student-dashboard-page'),
    path('count-attdnce/', views.counts, name='count-attdnce-page'),
    path('add-class/', views.add_class, name='add-class-page'),
    path('student-form/', views.student_form, name='student-form-page'),
    path('attendence/<str:brnch>/<int:sem>/<str:sec>/',views.attendence_sheet, name='attendence-page'),
    path('remove/<str:brnch>/<int:sem>/<str:sec>/',views.rm_clss, name='remove-class-page'),
    path('teacher-form/', views.teacher_form, name='teacher-form-page'),
    path('feedback-form/', views.feedback, name='feedback-page'),
    path('check_user_reg/', views.check_user_registered, name='check-user-reg'),
    path('login/', auth_views.LoginView.as_view(template_name='attendence/login.html'),name='login-page'),
    path('logout/', auth_views.LogoutView.as_view(template_name='attendence/logout.html'), name='logout-page'),
    path('idonno/<str:type_>/', views.idonno, name='idonno-page'),
    path('google645cd8e508c990d1.html/',views.google_verification, name='google'),
    path('marksStudent/<str:brnch>/<int:sem>/<str:sec>/',views.studMarks, name='marks-student-page'),
    path('marks-submit/<int:sem>/<str:sec>/<str:branch>/<str:subject>/',views.marksSub, name='marks-page'),
    # path('marks-submit/<str:username>/<int:sem>/<str:sec>/<str:branch>/<str:subject>/',views.marksSub, name='marks-page'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
