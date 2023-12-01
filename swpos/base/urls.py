from django.urls import path
from . import views

urlpatterns = [
    path('', views.base_view, name='base'),
    # 다른 URL 패턴들을 정의할 수 있음
    path('student/', views.student_view, name='student_page'),
    path('f_login/',views.faculty_login, name='login_page'),
    path('f_add_post/',views.faculty_add_poster, name = 'adding_page'),
    path('application/',views.application, name = 'apply'),
    path('delete_position/<int:position_id>/', views.delete_position, name='delete_position'),
    path('applicants/', views.applicants, name='applicants'),
    path('interview/<int:applicant_id>/<int:position_id>/', views.interview, name='interview')
]