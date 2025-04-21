from django.db import models
from django.contrib.auth.models import User

class Despesa(models.Model):
    descricao = models.CharField(max_length=100)
    favorecido = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    dataVencimento = models.DateField()
    categoria = models.CharField(max_length=50)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.descricao} - {self.usuario.username}"