from rest_framework import serializers
from Control.models import *

class DispositivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispositivo
        fields = ('dis_id', 'dis_nombre', 'dis_mac', 'dis_estado',)

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ('sen_id','sen_nombre','sen_unidadmedida','sen_localizacion','sen_estado','sen_tipo','dis_id',)

class ActuadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actuador
        fields = ('act_id', 'act_nombre', 'act_localizacion','act_funcion','act_estado','dis_id',)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name','last_name', 'email','is_active')



