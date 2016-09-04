from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class Empresa(models.Model):
    emp_id = models.AutoField(primary_key=True)
    emp_nombre=models.CharField(max_length=20,null=False)
    EST_CHOICES = (
        (u'a', u'Activo'),
        (u'i', u'Inactivo'),
    )
    emp_estado = models.CharField(max_length=1, choices=EST_CHOICES, default='a')

    def __str__(self):
        return self.emp_nombre

class Perfil(models.Model):
    usuario = models.OneToOneField(User)
    emp_id = models.ForeignKey(Empresa)
    def __str__(self):
        return self.usuario.username

class Dispositivo(models.Model):
    dis_id = models.AutoField(primary_key=True)
    dis_nombre=models.CharField(max_length=20,null=False)
    dis_mac=models.CharField(max_length=100,null=False)
    EST_CHOICES = (
        (u'a', u'Activo'),
        (u'i', u'Inactivo'),
    )
    dis_estado = models.CharField(max_length=1, choices=EST_CHOICES, default='a')
    emp_id = models.ForeignKey(Empresa)

    def __str__(self):
        return self.dis_nombre

class Pines(models.Model):
    pin_id = models.AutoField(primary_key=True)
    pin_nombre=models.CharField(max_length=20)
    pin_tipo=models.CharField(max_length=100)
    dis_id = models.ForeignKey(Dispositivo)

class Actuador(models.Model):
    act_id = models.AutoField(primary_key=True)
    act_nombre=models.CharField(max_length=20)
    act_localizacion=models.CharField(max_length=100)

    TIP_CHOICES = (
        (u'a', u'Automatico'),
        (u'm', u'Manual'),
    )

    FUN_CHOICES = (
        (u'e', u'Encendido'),
        (u'a', u'Apagado'),
    )

    EST_CHOICES = (
        (u'a', u'Activo'),
        (u'i', u'Inactivo'),
    )

    act_tip = models.CharField(max_length=1, choices=TIP_CHOICES, default='a')
    act_funcion = models.CharField(max_length=1, choices=FUN_CHOICES, default='a')
    act_estado = models.CharField(max_length=1, choices=EST_CHOICES, default='a')
    dis_id = models.ForeignKey(Dispositivo)

    def __str__(self):
        return self.act_nombre

class Sensor(models.Model):
    sen_id = models.AutoField(primary_key=True)
    sen_nombre=models.CharField(max_length=20)
    sen_unidadmedida=models.CharField(max_length=100)
    sen_localizacion=models.CharField(max_length=100)
    EST_CHOICES = (
        (u'a', u'Activo'),
        (u'i', u'Inactivo'),
    )

    TIP_CHOICES = (
        (u'a', u'Activador'),
        (u'i', u'Informativo'),
    )
    sen_estado = models.CharField(max_length=1, choices=EST_CHOICES, default='a')
    sen_tipo = models.CharField(max_length=1, choices=TIP_CHOICES, default='a')
    dis_id = models.ForeignKey(Dispositivo)

    def __str__(self):
        return self.sen_nombre

class Regla(models.Model):
    sen_id=models.ForeignKey(Sensor)
    act_id=models.ForeignKey(Actuador)

class DispositivoActuador(models.Model):
    dis_id=models.ForeignKey(Dispositivo)
    act_id=models.ForeignKey(Actuador)
    pin = models.CharField(max_length=2)

class DispositivoSensor(models.Model):
    dis_id = models.ForeignKey(Dispositivo)
    sen_id=models.ForeignKey(Sensor)
    pin = models.CharField(max_length=2)


class Registro(models.Model):
    reg_id=models.AutoField(primary_key=True)
    reg_fecha_hora=models.CharField(max_length=60)
    reg_descripcion=models.CharField(max_length=60)
    id=models.ForeignKey(User)
    act_id = models.ForeignKey(Actuador)

def __str__(self):
    return self.reg_fecha_hora
