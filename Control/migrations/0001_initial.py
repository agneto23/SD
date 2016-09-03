# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Actuador',
            fields=[
                ('act_id', models.AutoField(primary_key=True, serialize=False)),
                ('act_nombre', models.CharField(max_length=20)),
                ('act_localizacion', models.CharField(max_length=100)),
                ('act_tip', models.CharField(max_length=1, choices=[('a', 'Automatico'), ('m', 'Manual')], default='a')),
                ('act_funcion', models.CharField(max_length=1, choices=[('e', 'Encendido'), ('a', 'Apagado')], default='a')),
                ('act_estado', models.CharField(max_length=1, choices=[('a', 'Activo'), ('i', 'Inactivo')], default='a')),
            ],
        ),
        migrations.CreateModel(
            name='Dispositivo',
            fields=[
                ('dis_id', models.AutoField(primary_key=True, serialize=False)),
                ('dis_nombre', models.CharField(max_length=20)),
                ('dis_mac', models.CharField(max_length=100)),
                ('dis_estado', models.CharField(max_length=1, choices=[('a', 'Activo'), ('i', 'Inactivo')], default='a')),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('emp_id', models.AutoField(primary_key=True, serialize=False)),
                ('emp_nombre', models.CharField(max_length=20)),
                ('emp_estado', models.CharField(max_length=1, choices=[('a', 'Activo'), ('i', 'Inactivo')], default='a')),
            ],
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('emp_id', models.ForeignKey(to='Control.Empresa')),
                ('usuario', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Registro',
            fields=[
                ('reg_id', models.AutoField(primary_key=True, serialize=False)),
                ('reg_fecha_hora', models.CharField(max_length=60)),
                ('reg_descripcion', models.CharField(max_length=60)),
                ('act_id', models.ForeignKey(to='Control.Actuador')),
                ('id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Regla',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('act_id', models.ForeignKey(to='Control.Actuador')),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('sen_id', models.AutoField(primary_key=True, serialize=False)),
                ('sen_nombre', models.CharField(max_length=20)),
                ('sen_unidadmedida', models.CharField(max_length=100)),
                ('sen_localizacion', models.CharField(max_length=100)),
                ('sen_estado', models.CharField(max_length=1, choices=[('a', 'Activo'), ('i', 'Inactivo')], default='a')),
                ('sen_tipo', models.CharField(max_length=1, choices=[('a', 'Activador'), ('i', 'Informativo')], default='a')),
                ('dis_id', models.ForeignKey(to='Control.Dispositivo')),
            ],
        ),
        migrations.CreateModel(
            name='UsuarioDispositivo',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('dis_id', models.ForeignKey(to='Control.Dispositivo')),
                ('username', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='regla',
            name='sen_id',
            field=models.ForeignKey(to='Control.Sensor'),
        ),
        migrations.AddField(
            model_name='actuador',
            name='dis_id',
            field=models.ForeignKey(to='Control.Dispositivo'),
        ),
    ]
