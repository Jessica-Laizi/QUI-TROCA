from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Campus(models.Model): 
    campus=models.CharField(max_length=50,null=False)
     
class Inventario(models.Model):
    nome=models.CharField(max_length=50,null=False)
    validade=models.DateField(null=True)
    quantidade=models.CharField(max_length=50,null=False)
    disponivel=models.CharField(max_length=50,null=False)
    descricao=models.TextField(null=False)
    marca=models.CharField(max_length=50,null=True)
    estado_de_uso=models.CharField(max_length=50,null=False)
    imagem=models.CharField(max_length=100,null=True)
    campus=models.ForeignKey(Campus, on_delete=models.CASCADE)
    
class Usuario(models.Model):
    matricula=models.CharField(max_length=15,null=False)    
    campus=models.ForeignKey(Campus, on_delete=models.CASCADE)
    status=models.CharField(max_length=50,null=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    ingresso=models.CharField(max_length=15,null=False) 
    