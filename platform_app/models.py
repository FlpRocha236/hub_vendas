from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField("Título", max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField("Descrição")
    thumbnail = models.ImageField(upload_to='courses/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    video_url = models.URLField(help_text="Link do vídeo (YouTube, Vimeo, Panda)")
    order = models.PositiveIntegerField(default=1, help_text="Ordem da aula no curso (1, 2, 3...)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order'] 

    def __str__(self):
        return f"{self.order} - {self.title}"

class Enrollment(models.Model):
    """Controla quem comprou o quê"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course') # Evita duplicidade de compra

class Lead(models.Model):
    name = models.CharField("Nome", max_length=100)
    email = models.EmailField("E-mail", unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"