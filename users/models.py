from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager
from cloudinary_storage.storage import MediaCloudinaryStorage

class CustomUser(AbstractUser):
    # Hacer username opcional y email como principal
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    email = models.EmailField('email address', unique=True)
    
    # Campos adicionales (opcionales)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
        default='profile_pics/default_avatar.png',
        storage=MediaCloudinaryStorage()
    )
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Configuración para login con email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # ← VACÍO, así no pide username
    
    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def get_display_name(self):
        """Retorna el nombre para mostrar: nombre completo o email"""
        if self.first_name:
            return f"{self.first_name} {self.last_name}".strip()
        return self.email.split('@')[0]
    
    def save(self, *args, **kwargs):
        """Auto-generar username si no existe"""
        if not self.username:
            # Usar parte del email como username
            self.username = self.email.split('@')[0]
        super().save(*args, **kwargs)