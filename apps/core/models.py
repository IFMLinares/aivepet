from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

DEPARTAMENT_CHOICES = (
        ('AD', 'admin'),
        ('SU', 'supervisor'),
        ('OP', 'operador'),
        ('CL', 'cliente'),
    )

class User(AbstractUser):
    role = models.CharField(max_length=2, choices=DEPARTAMENT_CHOICES)
    company_name = models.CharField(max_length=150, verbose_name='Nombre de la empresa', blank=True, null=True)
    rif = models.CharField(max_length=150, verbose_name='RIF', blank=True, null=True)
    direction = models.CharField(max_length=150, verbose_name='Dirección', blank=True, null=True)
    phone_number = models.CharField(max_length=150, verbose_name='Número de teléfono', blank=True, null=True)

    class Meta:
        db_table = 'auth_user'
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
