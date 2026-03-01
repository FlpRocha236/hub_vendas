from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Lesson, Lead, Enrollment
from .forms import CourseForm, LessonForm, LeadForm
from django.contrib.auth.decorators import login_required, user_passes_test
# IMPORTAÇÃO QUE FALTAVA:
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# --- FUNÇÕES AUXILIARES ---
def is_staff(user):
    return user.is_staff

# --- PÁGINAS PÚBLICAS ---

def landing_page(request):
    success = False
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
            form = LeadForm()
    else:
        form = LeadForm()

    return render(request, 'platform/landing_page.html', {
        'form': form, 
        'success': success
    })

# --- ÁREA DO ALUNO ---

@login_required
def dashboard(request):
    # Lista apenas matrículas do usuário logado
    enrollments = Enrollment.objects.filter(user=request.user)
    return render(request, 'platform/dashboard.html', {'enrollments': enrollments})

@login_required
def course_view(request, slug):
    course = get_object_or_404(Course, slug=slug)
    lessons = Lesson.objects.filter(course=course).order_by('order')
    
    active_lesson_id = request.GET.get('aula')
    if active_lesson_id:
        active_lesson = get_object_or_404(Lesson, id=active_lesson_id)
    else:
        active_lesson = lessons.first()

    return render(request, 'platform/course_view.html', {
        'course': course,
        'lessons': lessons,
        'active_lesson': active_lesson
    })

# --- ÁREA STAFF (ADMIN) ---

@login_required
@user_passes_test(is_staff)
def staff_dashboard(request):
    courses = Course.objects.all().prefetch_related('lessons')
    course_form = CourseForm()
    lesson_form = LessonForm()
    
    return render(request, 'platform/staff_dashboard.html', {
        'courses': courses,
        'course_form': course_form,
        'lesson_form': lesson_form
    })

@login_required
@user_passes_test(is_staff)
def save_course(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        
        if course_id: # Edição
            course = get_object_or_404(Course, id=course_id)
            form = CourseForm(request.POST, request.FILES, instance=course)
        else: # Criação
            form = CourseForm(request.POST, request.FILES)
            
        if form.is_valid():
            form.save()
            
    return redirect('staff_dashboard')

@login_required
@user_passes_test(is_staff)
def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.delete()
    return redirect('staff_dashboard')

@login_required
@user_passes_test(is_staff)
def save_lesson(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        lesson_id = request.POST.get('lesson_id')
        
        if lesson_id: # Edição
            lesson = get_object_or_404(Lesson, id=lesson_id)
            form = LessonForm(request.POST, instance=lesson)
        else: # Criação
            form = LessonForm(request.POST)
        
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            
    return redirect('staff_dashboard')

@login_required
@user_passes_test(is_staff)
def delete_lesson(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    lesson.delete()
    return redirect('staff_dashboard')

# Rota legada
def create_course(request):
    return redirect('staff_dashboard')

# --- LOGOUT CUSTOMIZADO ---
def custom_logout(request):
    logout(request)
    return redirect('landing_page')

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        passw = request.POST.get('password')
        
        # Tenta autenticar o usuário
        user = authenticate(request, username=username, password=passw)
        
        if user is not None:
            login(request, user)
            
            # Redirecionamento Inteligente
            if user.is_staff:
                return redirect('staff_dashboard')
            else:
                return redirect('dashboard')
        else:
            # Se errou a senha
            messages.error(request, "Usuário ou senha incorretos.")
            return redirect('landing_page')
            
    return redirect('landing_page')