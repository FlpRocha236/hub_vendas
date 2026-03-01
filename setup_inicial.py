import os
import django
import requests
from django.core.files.base import ContentFile

# Configuração para rodar fora do manage.py shell tradicional
# (Isso garante que o script funcione independente de como for chamado)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings') # Ajuste 'core' se o nome da sua pasta de settings for outro
try:
    django.setup()
except:
    pass

from django.contrib.auth.models import User
from platform_app.models import Course, Lesson, Enrollment

print("🚀 Iniciando configuração automática...")

# 1. PEGAR (OU CRIAR) O ALUNO
student, created = User.objects.get_or_create(username='aluno_teste', email='aluno@teste.com')
if created or not student.check_password('aluno123'):
    student.set_password('aluno123')
    student.save()
print("✅ Aluno 'aluno_teste' pronto (Senha: aluno123).")

# 2. CRIAR/ATUALIZAR O CURSO COM CAPA BONITA
image_url = "https://images.unsplash.com/photo-1587620962725-abab7fe55159?q=80&w=1000&auto=format&fit=crop"

course, created = Course.objects.get_or_create(
    slug="curso-python-pro",
    defaults={
        'title': "Python PRO: Do Zero ao Fullstack",
        'description': "Domine a linguagem mais usada do mundo. Aprenda Django, API Rest, Automação e Ciência de Dados neste curso completo.",
        'price': 997.00
    }
)

# Tenta baixar a imagem
try:
    response = requests.get(image_url, timeout=10)
    if response.status_code == 200:
        course.thumbnail.save('python_cover.jpg', ContentFile(response.content), save=True)
        print("✅ Capa HD aplicada ao curso.")
    else:
        print("⚠️ Não foi possível baixar a imagem (Status code diferente de 200).")
except Exception as e:
    print(f"⚠️ Erro ao baixar imagem: {e}")

# 3. CRIAR AULAS COM VÍDEO REAL
lessons_data = [
    {
        "title": "01. Bem-vindo ao Futuro",
        "desc": "Entenda como este curso vai mudar sua carreira.",
        "url": "https://www.youtube.com/embed/S9uPNppGsGo",
        "order": 1
    },
    {
        "title": "02. Configurando o Ambiente",
        "desc": "Instalando VSCode, Python e configurando o Virtualenv.",
        "url": "https://www.youtube.com/embed/W6NZfCO5SIk",
        "order": 2
    },
    {
        "title": "03. Sua Primeira Automação",
        "desc": "Criando um bot que trabalha por você.",
        "url": "https://www.youtube.com/embed/t8pPdKYpowI",
        "order": 3
    }
]

# Limpa aulas antigas para evitar duplicidade
course.lessons.all().delete()

for data in lessons_data:
    Lesson.objects.create(
        course=course,
        title=data["title"],
        description=data["desc"],
        video_url=data["url"],
        order=data["order"]
    )
print(f"✅ {len(lessons_data)} aulas criadas com vídeos reais.")

# 4. GARANTIR MATRÍCULA
Enrollment.objects.get_or_create(user=student, course=course)
print("✅ Aluno matriculado com sucesso.")
print("🏁 Finalizado! Pode testar no navegador.")