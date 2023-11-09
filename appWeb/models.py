from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils import timezone

# Create your models here.

class InfoMed(models.Model):
    codigo = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=300)
    concentracion = models.CharField(max_length=300)
    presentacion = models.CharField(max_length=300)

    def __str__(self):
        return self.nombre

class AdminMed(models.Model):
    codigo = models.ForeignKey(InfoMed, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha = models.DateField()

    def __str__(self):
        return f"AdminMed #{self.id}"
    
    

class StockMed(models.Model):
    codigo = models.ForeignKey(InfoMed, on_delete=models.CASCADE)
    stock = models.IntegerField()

    def __str__(self):
        return f"StockMed #{self.id}"


class demanda_diarias(models.Model):
    codigo = models.ForeignKey(InfoMed, on_delete=models.CASCADE)
    entregado = models.IntegerField()
    no_entregado = models.IntegerField()
    fecha = models.DateField()
    
    class Meta:
        db_table = 'demanda_diaria_db'


    

    

class SaldoAnterior(models.Model):
    codigo = models.ForeignKey(InfoMed, on_delete=models.CASCADE)
    saldoAnterior = models.IntegerField()
    fecha = models.DateField()

    def __str__(self):
        return f"SaldoAnterior #{self.id}"
    
   
class admin_indi(models.Model):
    codigo= models.IntegerField(primary_key=True)
    nombre= models.CharField(max_length=300)
    metaIndi= models.CharField(max_length=10)

    def __str__(self):
       return self.nombre

class indi_mensuales(models.Model):
    codigo = models.ForeignKey(admin_indi, on_delete=models.CASCADE)
    metaMes = models.IntegerField()
    fecha = models.DateField()

    def __str__(self):
        return f"{self.codigo.nombre} - {self.fecha}"



class DemandaReal(models.Model):
    codigo = models.ForeignKey(InfoMed, on_delete=models.CASCADE)
    demanda_real = models.IntegerField()
    fecha = models.DateField()

    def __str__(self):
        return f"DemandaReal #{self.id}"


#@receiver(post_save, sender=demanda_diarias)

class prueba(models.Model):
    demanda_realidades = models.IntegerField()