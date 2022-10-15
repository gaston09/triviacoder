from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Usuario(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    email = models.EmailField()
    #pwd = models.TextField()

    def __str__(self):
        return f"Nombre:{self.nombre}  -  Apellido: {self.apellido} - Email: {self.email}"

class CuestionarioTecnologia(models.Model):
    pregunta = models.TextField()
    respuesta = models.TextField()

    def __str__(self):
        return f" Pregunta:{self.pregunta}  -  Respuesta: {self.respuesta}"

class CuestionarioNaturales(models.Model):
    pregunta = models.TextField()
    respuesta = models.TextField()

    def __str__(self):
        return f" Pregunta:{self.pregunta}  -  Respuesta: {self.respuesta}"

class CuestionarioSociales(models.Model):
    pregunta = models.TextField()
    respuesta = models.TextField()

    def __str__(self):
        return f" Pregunta:{self.pregunta}  -  Respuesta: {self.respuesta}"
    
class Avatar(models.Model):
    #vinculo con el usuario
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #subcarpeta Avatares de media
    image = models.ImageField(upload_to='avatares', null = True, blank = True)