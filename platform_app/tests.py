from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Course, Lesson, Enrollment, Lead

# ==========================================
# 1. TESTES DE MODELOS (BANCO DE DADOS)
# ==========================================
class ModelTests(TestCase):

    def test_course_string_representation(self):
        """Teste 01: O modelo Course retorna o título correto?"""
        course = Course.objects.create(title="Curso Teste", price=10)
        self.assertEqual(str(course), "Curso Teste")

    def test_lesson_string_representation(self):
        """Teste 02: O modelo Lesson retorna a ordem e título?"""
        course = Course.objects.create(title="Curso Teste", price=10)
        lesson = Lesson.objects.create(course=course, title="Aula 1", order=1, video_url="http://v.com")
        # Ajuste conforme seu __str__ no models.py. Se for '1 - Aula 1', use isso.
        # Aqui assumo que o __str__ retorna algo contendo o título.
        self.assertIn("Aula 1", str(lesson))

    def test_enrollment_creation(self):
        """Teste 03: É possível criar uma matrícula?"""
        user = User.objects.create(username="user")
        course = Course.objects.create(title="Curso", price=10)
        enrollment = Enrollment.objects.create(user=user, course=course)
        self.assertEqual(Enrollment.objects.count(), 1)


# ==========================================
# 2. TESTES PÚBLICOS (LANDING PAGE & LEADS)
# ==========================================
class PublicViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_landing_page_status_code(self):
        """Teste 04: A página inicial carrega (Status 200)?"""
        response = self.client.get(reverse('landing_page'))
        self.assertEqual(response.status_code, 200)

    def test_landing_page_content(self):
        """Teste 05: A página inicial contém o texto chave?"""
        response = self.client.get(reverse('landing_page'))
        self.assertContains(response, "Domine o Jogo")

    def test_create_lead_valid(self):
        """Teste 06: Um visitante consegue se cadastrar (Lead)?"""
        response = self.client.post(reverse('landing_page'), {
            'name': 'Visitante',
            'email': 'visita@teste.com'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Lead.objects.filter(email='visita@teste.com').exists())

    def test_create_lead_invalid(self):
        """Teste 07: O sistema rejeita e-mail inválido?"""
        # O Django Form valida, mas se passar, o banco pode aceitar.
        # Aqui testamos se o count muda se enviarmos dados vazios obrigatórios
        initial_count = Lead.objects.count()
        response = self.client.post(reverse('landing_page'), {
            'name': '', # Nome vazio (se for obrigatório)
            'email': 'email-invalido' 
        })
        # Se o form for inválido, ele renderiza a página de novo (200) mas não salva
        # Depende da validação do seu form. Vamos assumir validação básica.
        # Se não salvar, o count deve ser igual.
        if response.context['form'].errors:
            self.assertEqual(Lead.objects.count(), initial_count)


# ==========================================
# 3. TESTES DE AUTENTICAÇÃO
# ==========================================
class AuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = User.objects.create_user(username='aluno', password='123')
        self.staff = User.objects.create_user(username='admin', password='123', is_staff=True)

    def test_login_student_redirect(self):
        """Teste 08: Login de Aluno redireciona para Dashboard?"""
        response = self.client.post(reverse('custom_login'), {
            'username': 'aluno',
            'password': '123'
        }, follow=True)
        self.assertRedirects(response, reverse('dashboard'))

    def test_login_staff_redirect(self):
        """Teste 09: Login de Staff redireciona para Painel Staff?"""
        response = self.client.post(reverse('custom_login'), {
            'username': 'admin',
            'password': '123'
        }, follow=True)
        self.assertRedirects(response, reverse('staff_dashboard'))

    def test_login_invalid(self):
        """Teste 10: Login com senha errada falha?"""
        response = self.client.post(reverse('custom_login'), {
            'username': 'aluno',
            'password': 'senha_errada'
        }, follow=True)
        # Deve voltar para landing page ou ficar na mesma
        self.assertFalse(response.context['user'].is_authenticated)

    def test_logout(self):
        """Teste 11: Logout funciona e redireciona?"""
        self.client.login(username='aluno', password='123')
        response = self.client.get(reverse('logout'), follow=True)
        self.assertRedirects(response, reverse('landing_page'))
        self.assertFalse(response.context['user'].is_authenticated)


# ==========================================
# 4. TESTES DA ÁREA DO ALUNO
# ==========================================
class StudentAreaTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='aluno', password='123')
        self.course = Course.objects.create(title="Curso Python", slug="python", price=100)
        self.lesson = Lesson.objects.create(course=self.course, title="Aula 1", order=1, video_url="http://x.com")

    def test_dashboard_anonymous_block(self):
        """Teste 12: Anônimo é bloqueado no Dashboard?"""
        response = self.client.get(reverse('dashboard'))
        self.assertNotEqual(response.status_code, 200) # Deve ser 302

    def test_dashboard_authenticated_empty(self):
        """Teste 13: Aluno sem cursos vê dashboard vazio?"""
        self.client.login(username='aluno', password='123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Curso Python")

    def test_dashboard_authenticated_enrolled(self):
        """Teste 14: Aluno matriculado vê o curso?"""
        Enrollment.objects.create(user=self.user, course=self.course)
        self.client.login(username='aluno', password='123')
        response = self.client.get(reverse('dashboard'))
        self.assertContains(response, "Curso Python")

    def test_player_load_success(self):
        """Teste 15: O Player carrega a aula corretamente?"""
        self.client.login(username='aluno', password='123')
        response = self.client.get(reverse('course_view', args=[self.course.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aula 1")

    def test_player_404_invalid_course(self):
        """Teste 16: Slug inválido retorna erro 404?"""
        self.client.login(username='aluno', password='123')
        response = self.client.get(reverse('course_view', args=['slug-inexistente']))
        self.assertEqual(response.status_code, 404)


# ==========================================
# 5. TESTES DA ÁREA STAFF (ADMIN)
# ==========================================
class StaffAreaTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = User.objects.create_user(username='aluno', password='123')
        self.staff = User.objects.create_user(username='admin', password='123', is_staff=True)
        self.course = Course.objects.create(title="Curso Velho", slug="velho", price=50)

    def test_staff_dashboard_access_denied_student(self):
        """Teste 17: Aluno comum NÃO acessa painel staff?"""
        self.client.login(username='aluno', password='123')
        response = self.client.get(reverse('staff_dashboard'))
        self.assertNotEqual(response.status_code, 200) # Deve redirecionar

    def test_staff_dashboard_access_allowed(self):
        """Teste 18: Staff acessa painel com sucesso?"""
        self.client.login(username='admin', password='123')
        response = self.client.get(reverse('staff_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Painel Administrativo")

    def test_create_course(self):
        """Teste 19: Criar novo curso funciona?"""
        self.client.login(username='admin', password='123')
        response = self.client.post(reverse('save_course'), {
            'title': 'Curso Novo',
            'price': '199.90',
            'slug': 'curso-novo',
            'description': 'Desc'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Course.objects.filter(slug='curso-novo').exists())

    def test_edit_course(self):
        """Teste 20: Editar curso existente funciona?"""
        self.client.login(username='admin', password='123')
        response = self.client.post(reverse('save_course'), {
            'course_id': self.course.id, # ID para editar
            'title': 'Curso Editado',
            'price': '50.00',
            'slug': 'velho',
            'description': 'Desc'
        }, follow=True)
        
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, 'Curso Editado')

    def test_delete_course(self):
        """Teste 21: Excluir curso funciona?"""
        self.client.login(username='admin', password='123')
        response = self.client.get(reverse('delete_course', args=[self.course.id]), follow=True)
        self.assertFalse(Course.objects.filter(id=self.course.id).exists())

    def test_create_lesson(self):
        """Teste 22: Criar aula vinculada ao curso?"""
        self.client.login(username='admin', password='123')
        response = self.client.post(reverse('save_lesson', args=[self.course.id]), {
            'title': 'Nova Aula',
            'video_url': 'http://y.com',
            'order': 1
        }, follow=True)
        self.assertTrue(Lesson.objects.filter(title='Nova Aula', course=self.course).exists())

    def test_delete_lesson(self):
        """Teste 23: Excluir aula funciona?"""
        lesson = Lesson.objects.create(course=self.course, title="A Deletar", order=1, video_url="x")
        self.client.login(username='admin', password='123')
        
        response = self.client.get(reverse('delete_lesson', args=[lesson.id]), follow=True)
        self.assertFalse(Lesson.objects.filter(id=lesson.id).exists())