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
                ('act_id', models.AutoField(serialize=False, primary_key=True)),
                ('act_nombre', models.CharField(max_length=20)),
                ('act_localizacion', models.CharField(max_length=100)),
                ('act_tip', models.CharField(default='a', max_length=1, choices=[('a', 'Automatico'), ('m', 'Manual')])),
                ('act_funcion', models.CharField(default='a', max_length=1, choices=[('e', 'Encendido'), ('a', 'Apagado')])),
                ('act_estado', models.CharField(default='a', max_length=1, choices=[('a', 'Activo'), ('i', 'Inactivo')])),
            ],
        ),
        migrations.CreateModel(
            name='Dispositivo',
            fields=[
                ('dis_id', models.AutoField(serialize=False, primary_key=True)),
                ('dis_nombre', models.CharField(max_length=20)),
                ('dis_mac', models.CharField(max_length=100)),
                ('dis_estado', models.CharField(default='a', max_length=1, choices=[('a', 'Activo'), ('i', 'Inactivo')])),
            ],
        ),
        migrations.CreateModel(
            name='DispositivoActuador',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('pin', models.CharField(max_length=2)),
                ('act_id', models.ForeignKey(to='Control.Actuador')),
                ('dis_id', models.ForeignKey(to='Control.Dispositivo')),
            ],
        ),
        migrations.CreateModel(
            name='DispositivoSensor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('pin', models.CharField(max_length=2)),
                ('dis_id', models.ForeignKey(to='Control.Dispositivo')),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('emp_id', models.AutoField(serialize=False, primary_key=True)),
                ('emp_nombre', models.CharField(max_length=20)),
                ('emp_estado', models.CharField(default='a', max_length=1, choices=[('a', 'Activo'), ('i', 'Inactivo')])),
            ],
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('emp_id', models.ForeignKey(to='Control.Empresa')),
                ('usuario', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pines',
            fields=[
                ('pin_id', models.AutoField(serialize=False, primary_key=True)),
                ('pin_nombre', models.CharField(max_length=20)),
                ('pin_tipo', models.CharField(max_length=100)),
                ('dis_id', models.ForeignKey(to='Control.Dispositivo')),
            ],
        ),
        migrations.CreateModel(
            name='Registro',
            fields=[
                ('reg_id', models.AutoField(serialize=False, primary_key=True)),
                ('reg_fecha_hora', models.CharField(max_length=60)),
                ('reg_descripcion', models.CharField(max_length=60)),
                ('act_id', models.ForeignKey(to='Control.Actuador')),
                ('id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Regla',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('act_id', models.ForeignKey(to='Control.Actuador')),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('sen_id', models.AutoField(serialize=False, primary_key=True)),
                ('sen_nombre', models.CharField(max_length=20)),
                ('sen_unidadmedida', models.CharField(max_length=100)),
                ('sen_localizacion', models.CharField(max_length=100)),
                ('sen_estado', models.CharField(default='a', max_length=1, choices=[('a', 'Activo'), ('i', 'Inactivo')])),
                ('sen_tipo', models.CharField(default='a', max_length=1, choices=[('a', 'Activador'), ('i', 'Informativo')])),
                ('dis_id', models.ForeignKey(to='Control.Dispositivo')),
            ],
        ),
        migrations.AddField(
            model_name='regla',
            name='sen_id',
            field=models.ForeignKey(to='Control.Sensor'),
        ),
        migrations.AddField(
            model_name='dispositivosensor',
            name='sen_id',
            field=models.ForeignKey(to='Control.Sensor'),
        ),
        migrations.AddField(
            model_name='dispositivo',
            name='emp_id',
            field=models.ForeignKey(to='Control.Empresa'),
        ),
        migrations.AddField(
            model_name='actuador',
            name='dis_id',
            field=models.ForeignKey(to='Control.Dispositivo'),
        ),
    ]
