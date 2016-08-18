"""SD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls import patterns, include, url

from Control.views import *

from servicioweb.views import *
from rest_framework.routers import DefaultRouter

from django.contrib import admin
# from django.contrib import admin

router = DefaultRouter()
router.register(r'dispositivos', DispositivoViewSet)
router.register(r'sensores', SensorViewSet)
router.register(r'actuadores', ActuadorViewSet)
router.register(r'usuarios', UserViewSet)


urlpatterns = patterns('',

    url(r'rest/', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^cerrar/$', 'django.contrib.auth.views.logout_then_login', name='logout'),

    url(r'^inicio/$', index_view, name='inicio'),

    url(r'^iot/ingresardispositivos/$',ingresardispositivos,name='ingresardispositivos'),
    url(r'^iot/editardispositivos/(?P<id>\d+)/$',editardispositivos,name='editardispositivos'),
    url(r'^iot/ingresaractuadores/$',ingresaractuadores,name='ingresaractuadores'),
    url(r'^iot/editaractuadores/(?P<id>\d+)/$',editaractuadores,name='editaractuadores'),
    url(r'^iot/ingresarsensores/$',ingresarsensores,name='ingresarsensores'),
    url(r'^iot/sensores/$',sensores,name='sensores'),

    url(r'^usuarios/ingresarempresas/$',ingresarempresas,name='ingresarempresas'),
    url(r'^usuarios/editarempresas/(?P<id>\d+)/$',editarempresas,name='editarempresas'),
    url(r'^usuarios/ingresarusuarios$', crear_usuario.as_view(),name='ingresarusuario'),
    url(r'^usuarios/editarusuarios/(?P<pk>\d+)/$',editUser_view.as_view(),name='editarusuarios'),

    url(r'^control/cargarregistros/$',cargarregistros,name='cargarregistros'),
    url(r'^control/registros/$',registros,name='registros'),
    url(r'^control/buscarregistros/$',buscarregistros,name='buscarregistros'),

    url(r'^iot/buscardispositivos/$',buscardispositivos,name='buscardispositivos'),
    url(r'^iot/buscaractuadores/$',buscaractuadores,name='buscaractuadores'),
    url(r'^iot/buscarsensores/$',buscarsensores,name='buscarsensores'),
    url(r'^iot/editarsensores/(?P<id>\d+)/$',editarsensores,name='editarsensores'),

    url(r'^iot/$',iot,name='iot'),


    url(r'^control/$',control,name='control'),

    url(r'^usuarios/$',usuarios,name='usuarios'),


    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls'))

)

