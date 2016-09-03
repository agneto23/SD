from django.shortcuts import render_to_response, RequestContext, redirect, HttpResponse,render,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from Control.models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from django.views.generic import FormView, ListView,UpdateView
import json
from django.core import serializers
import time
from datetime import datetime
import base64
from django.db import transaction
import json

import random
import time
import paho.mqtt.client as mqtt

import time



def index_view(request):
    return render_to_response('inicio.html',context=RequestContext(request))


#def login_view(request):
#   return  render_to_response('login.html',context=RequestContext(request))




@login_required(login_url='/')
def control(request):

    act = Actuador.objects.all()
    reg = Registro.objects.order_by("-reg_id")

    return render_to_response('control.html', {'act': act, 'reg': reg},context_instance=RequestContext(request))

@login_required(login_url='/')
def iot(request):


    dis = Dispositivo.objects.all()
    act = Actuador.objects.all()
    sen = Sensor.objects.all()
    return render_to_response('iot.html',{'dis':dis,'sen':sen,'act':act}, context_instance=RequestContext(request))



@login_required(login_url='/')
def usuarios(request):

    emp = Empresa.objects.all()
    usu = User.objects.all()
    per = Perfil.objects.all()
    return render_to_response('usuarios.html', {'emp': emp, 'usu': usu, 'per': per},context_instance=RequestContext(request))


class crear_usuario(FormView):
    form_class = UserForm
    template_name = 'ingresarusuario.html'
    success_url ='/usuarios/'
    def form_valid(self, form):
        try:
            with transaction.atomic():
                user = form.save()
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']
                user.is_superuser = form.cleaned_data['is_superuser']

                user.is_active = form.cleaned_data['is_active']
                user.save()
                perfil = Perfil()
                print("" + str(user))
                perfil.usuario = user
                print("" + str(user.id))
                perfil.emp_id = form.cleaned_data['emp_id']
                perfil.save()
                return super(crear_usuario, self).form_valid(form)
        except Exception as e:
            return redirect('ingresarusuario')

def editar_usuario(request,id):
    emp=Empresa.objects.all()
    usuario=get_object_or_404(User,pk=id)
    cont={}
    perfil=get_object_or_404(Perfil,usuario=usuario)
    id_perfil = perfil.id
    var = ""
    var2 = ""
    cont={'empresa':emp,'usuario':usuario,'perfil':perfil}
    if request.method=='POST':
        try:
            with transaction.atomic():
                print("entro try")

                if request.POST['yapues'] == "True":
                   var = True
                else:
                   var = False

                if request.POST['estado1'] == "True":
                    var2 = True
                else:
                    var2 = False

                usuario = User(id=id,
                               username=request.POST['txtUsername'],
                               password=usuario.password,
                               is_superuser=var,
                               first_name=request.POST['txtFirstname'],
                               last_name=request.POST['txtLastname'],
                               email=request.POST['txtEmail'],
                               is_staff=usuario.is_staff,
                               is_active=var2,
                               )
                empr=Empresa.objects.get(pk=request.POST['emp_id'])

                perfil = Perfil(id=id_perfil,
                                usuario=usuario,
                                emp_id=empr,
                                )

                usuario.save()
                perfil.save()
                print("listo")
                return redirect('usuarios')

        except Exception as error:

            return render_to_response('editarusuarios.html', cont, context_instance=RequestContext(request))
    return render_to_response('editarusuarios.html', cont, context_instance=RequestContext(request))


class editUser_view(UpdateView):
    model = User
    fields = ('username','password','first_name','last_name','email','is_superuser','is_active')
    template_name = 'editarusuarios.html'
    success_url = '/usuarios/'


@login_required(login_url='/')
def ingresarempresas(request):
    if request.method == 'POST':

        try:
            with transaction.atomic():
                emp = Empresa(emp_nombre=request.POST['emp_nombre'], emp_estado=request.POST['emp_estado'], )

                emp.save()
                return redirect('usuarios')

        except:
            return render_to_response('ingresarempresas.html', context=RequestContext(request))

    return render_to_response('ingresarempresas.html', context=RequestContext(request))


@login_required(login_url='/')
def ingresardispositivos(request):
    if request.method == 'POST':

        try:
            with transaction.atomic():
                motes = Dispositivo(dis_nombre=request.POST['dis_nombre'],
                                    dis_mac=request.POST['dis_mac'], dis_estado=request.POST['dis_estado'], )

                motes.save()
                return redirect('iot')

        except:
            return render_to_response('ingresardispositivos.html', context=RequestContext(request))

    return render_to_response('ingresardispositivos.html', context=RequestContext(request))


@login_required(login_url='/')
def editarempresas(request,id):
    if request.method == 'POST':

        try:
            with transaction.atomic():
                emp = Empresa(emp_id=id,emp_nombre=request.POST['emp_nombre'], emp_estado=request.POST['emp_estado'], )

                emp.save()

                return redirect('usuarios')
        except:
            return render_to_response('editarempresas.html', context=RequestContext(request))

    emp = Empresa.objects.get(pk=id)
    return render_to_response('editarempresas.html',{'emp':emp}, context_instance=RequestContext(request))

@login_required(login_url='/')
def editardispositivos(request,id):
    if request.method == 'POST':

        try:
            with transaction.atomic():
                motes = Dispositivo(dis_id=id,dis_nombre=request.POST['dis_nombre'],
                                    dis_mac=request.POST['dis_mac'], dis_estado=request.POST['dis_estado'], )

                motes.save()

                return redirect('iot')
        except:
            return render_to_response('editardispositivos.html', context=RequestContext(request))

    dis = Dispositivo.objects.get(pk=id)
    return render_to_response('editardispositivos.html',{'dis':dis}, context_instance=RequestContext(request))

@login_required(login_url='/')
def ingresaractuadores(request):
    if request.method == 'POST':

        try:
            with transaction.atomic():

                dis = Dispositivo.objects.get(pk=request.POST["dis_id"])
                act = Actuador(act_nombre=request.POST['act_nombre'],
                               act_localizacion=request.POST['act_localizacion'],
                               act_tip=request.POST['act_tip'],
                               act_funcion=request.POST['act_funcion'],
                               act_estado = request.POST['act_estado'],
                               dis_id=dis)

                act.save()



                return redirect('iot')
        except:
            return render_to_response('ingresaractuadores.html', context=RequestContext(request))

    dis = Dispositivo.objects.all()
    return render_to_response('ingresaractuadores.html',{'dis':dis}, context_instance=RequestContext(request))

@login_required(login_url='/')
def editaractuadores(request,id):


    if request.method == 'POST':

        try:
            with transaction.atomic():
                dis = Dispositivo.objects.get(pk=request.POST["dis_id"])
                act = Actuador(act_id=id,act_nombre=request.POST['act_nombre'],
                               act_localizacion=request.POST['act_localizacion'],
                               act_tip=request.POST['act_tip'],
                               act_funcion=request.POST['act_funcion'],
                               act_estado = request.POST['act_estado'],
                               dis_id=dis,)

                act.save()

                return redirect('iot')
        except:
            return render_to_response('editaractuadores.html', context=RequestContext(request))

    act = Actuador.objects.get(pk=id)
    dis = Dispositivo.objects.all()
    return render_to_response('editaractuadores.html',{'act':act,'dis':dis}, context_instance=RequestContext(request))

@login_required(login_url='/')
def ingresarsensores(request):
    if request.method == 'POST':

        try:
            with transaction.atomic():
                dis = Dispositivo.objects.get(pk=request.POST["dis_id"])
                sen = Sensor(sen_nombre=request.POST['sen_nombre'],
                             sen_unidadmedida=request.POST['sen_unidadmedida'],
                             sen_localizacion=request.POST['sen_localizacion'], sen_estado=request.POST['sen_estado'],
                             sen_tipo = request.POST['sen_tipo'],
                             dis_id=dis,)

                sen.save()



                return redirect('iot')
        except:
            return render_to_response('ingresarsensores.html', context=RequestContext(request))

    dis = Dispositivo.objects.all()
    return render_to_response('ingresarsensores.html',{'dis':dis}, context_instance=RequestContext(request))

@login_required(login_url='/')
def sensores(request):


    sen = Sensor.objects.filter(dis_id_id = request.GET["codigo"])
    return render_to_response('sensores.html',{'sen':sen}, context_instance=RequestContext(request))

@login_required(login_url='/')
def registros(request):
    mensajes_Error = {}
    datosJson = {}
    a = request.GET["codigo"]
    cod = int(a)
    actua = Actuador.objects.get(pk=cod)
    u = request.GET["usuario"]
    fun = actua.act_funcion

    if fun == 'e':

        with transaction.atomic():
            act = Actuador.objects.get(pk=a)
            usu = User.objects.get(pk=u)
            reg = Registro(reg_fecha_hora=""+time.strftime("%c"),
                           reg_descripcion="Apagado", act_id=act,id=usu, )
            reg.save()

            actu = Actuador.objects.get(pk=cod)

            disp = Dispositivo.objects.get(pk=actu.dis_id_id)

            act = Actuador(act_id=cod,act_nombre=actu.act_nombre,
                           act_localizacion=actu.act_localizacion,
                           act_tip=actu.act_tip,
                           act_funcion="a",
                           act_estado = actu.act_estado,
                           dis_id=disp,)
            act.save()

            """try:

                # datos = ""+{"act_id": cod, "act_funcion": "e"}.__str__()

                datos2 = json.dumps({"act_id": cod, "act_funcion": "a"})

                # datos1 = {"datos": datos}


                timestamp = int(time.time())
                broker = '25.104.220.184'
                port = 1883

                #"********************Cargando datos de JSON******************"
                # datosJson = {"datos": datos}
                # *********************MQTT PUBLICADOR******************
                topic = 'SMARTHOME_ACTUADORES'
                # message = datosJson["datos"]
                mqttclient = mqtt.Client("mqtt-panel-test", protocol=mqtt.MQTTv311)
                mqttclient.username_pw_set("smarthome", "ABC123..")
                mqttclient.connect(broker, port=int(port))
                mqttclient.publish(topic, datos2)


            except Exception as error:
                print("Error al guardar-->transaccion" + str(error))"""



    else:

        with transaction.atomic():
            act = Actuador.objects.get(pk=a)
            usu = User.objects.get(pk=u)
            reg = Registro(reg_fecha_hora="" + time.strftime("%c"),
                           reg_descripcion="Encendido", act_id=act, id=usu, )
            reg.save()

            actu = Actuador.objects.get(pk=cod)
            print("aqui")
            disp = Dispositivo.objects.get(pk=actu.dis_id_id)

            act = Actuador(act_id=cod, act_nombre=actu.act_nombre,
                           act_localizacion=actu.act_localizacion,
                           act_tip=actu.act_tip,
                           act_funcion="e",
                           act_estado=actu.act_estado,
                           dis_id=disp, )
            act.save()

            """ try:

                #datos = ""+{"act_id": cod, "act_funcion": "e"}.__str__()

                datos2 = json.dumps({"act_id": cod, "act_funcion": "e"})

                #datos1 = {"datos": datos}


                timestamp = int(time.time())
                broker = '25.104.220.184'
                port = 1883

                "********************Cargando datos de JSON******************"
                #datosJson = {"datos": datos}
                # *********************MQTT PUBLICADOR******************
                topic = 'SMARTHOME_ACTUADORES'
                #message = datosJson["datos"]
                mqttclient = mqtt.Client("mqtt-panel-test", protocol=mqtt.MQTTv311)
                mqttclient.username_pw_set("smarthome", "ABC123..")
                mqttclient.connect(broker, port=int(port))
                mqttclient.publish(topic, datos2)


            except Exception as error:
                print("Error al guardar-->transaccion" + str(error))* /"""


    return render_to_response('registros.html', context_instance=RequestContext(request))


@login_required(login_url='/')
def cargarregistros(request):

    reg = Registro.objects.order_by("-reg_id")
    return render_to_response('registros.html',{'reg':reg}, context_instance=RequestContext(request))


@login_required(login_url='/')
def buscarregistros(request):

    reg = Registro.objects.filter(reg_descripcion__contains= request.GET["buscar1"])
    return render_to_response('buscarregistros.html',{'reg':reg}, context_instance=RequestContext(request))

@login_required(login_url='/')
def buscardispositivos(request):

    dis = Dispositivo.objects.filter(dis_nombre__contains = request.GET["buscar"])
    return render_to_response('buscardispositivos.html',{'dis':dis}, context_instance=RequestContext(request))

@login_required(login_url='/')
def buscaractuadores(request):

    act = Actuador.objects.filter(act_nombre__contains = request.GET["buscar"])
    return render_to_response('buscaractuadores.html',{'act':act}, context_instance=RequestContext(request))

@login_required(login_url='/')
def buscarsensores(request):

    sen = Sensor.objects.filter(sen_nombre__contains = request.GET["buscar"])
    return render_to_response('buscarsensores.html',{'sen':sen}, context_instance=RequestContext(request))

@login_required(login_url='/')
def editarsensores(request,id):
    if request.method == 'POST':

        try:
            with transaction.atomic():
                dis = Dispositivo.objects.get(pk=request.POST["dis_id"])
                sen = Sensor(sen_id=id,sen_nombre=request.POST['sen_nombre'],
                             sen_unidadmedida=request.POST['sen_unidadmedida'],
                             sen_localizacion=request.POST['sen_localizacion'], sen_estado=request.POST['sen_estado'],
                             sen_tipo = request.POST['sen_tipo'],
                             dis_id=dis,)
                sen.save()

                return redirect('iot')
        except:
            return render_to_response('editarsensores.html', context=RequestContext(request))

    dis = Dispositivo.objects.all()
    sen = Sensor.objects.get(pk=id)
    return render_to_response('editarsensores.html',{'sen':sen,'dis':dis}, context_instance=RequestContext(request))