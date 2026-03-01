# platform_app/admin.py
from django.contrib import admin
from .models import Lead, Course, Lesson, Enrollment

# Configuração para cadastrar aulas DENTRO do curso (Fica muito mais rápido)
class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1 # Mostra 1 campo extra vazio para adicionar aula rápida

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline] # Isso faz as aulas aparecerem dentro da tela do Curso
    #list_display = ('title', 'price', 'created_at')
    list_display = ('title', 'price')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)

# Mantenha os outros registros (Lead, Enrollment) como estavam
admin.site.register(Lead)
admin.site.register(Enrollment)