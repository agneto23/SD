from django.shortcuts import render
from Control.models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth import authenticate, login


class DispositivoViewSet(viewsets.ModelViewSet):
    serializer_class = DispositivoSerializer
    queryset = Dispositivo.objects.all()

class SensorViewSet(viewsets.ModelViewSet):
    serializer_class = SensorSerializer
    queryset = Sensor.objects.all()

class ActuadorViewSet(viewsets.ModelViewSet):
    allowed_methods = ('GET', 'POST', 'PUT', 'PATCH')
    serializer_class = ActuadorSerializer
    queryset = Actuador.objects.all()

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


