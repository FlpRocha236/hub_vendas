from django.urls import path
from . import views

urlpatterns = [
    # Páginas Públicas e Aluno
    path('', views.landing_page, name='landing_page'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('course/<slug:slug>/', views.course_view, name='course_view'),
    
    # Área Staff
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    
    # Ações de Curso
    path('staff/course/save/', views.save_course, name='save_course'),
    path('staff/course/delete/<int:pk>/', views.delete_course, name='delete_course'),
    
    # Ações de Aula
    path('staff/lesson/save/<int:course_id>/', views.save_lesson, name='save_lesson'),
    path('staff/lesson/delete/<int:pk>/', views.delete_lesson, name='delete_lesson'),
    
    # Rota legada (só para garantir que não quebre se alguém acessar)
    path('create_course/', views.staff_dashboard, name='create_course'),
    
    path('login/', views.custom_login, name='custom_login'),
    path('logout/', views.custom_logout, name='logout'),
]