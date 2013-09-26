#!/usr/bin/python
# -*- coding: utf-8 -*-
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.core.validators import validate_email,ValidationError
from django.views.generic import ListView, DetailView
from datetime import datetime
from models import Incidence, Entity
# Portada, si el usuario está logged lo redirige a sus incidencias, si no le muestra
# un mensaje de bienvenida y un form to login.
def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('SGIAPP:userilist'))
    else:        # Do something for anonymous users.
        return render(request,'SGIAPP/home.html',{})

# Procesa el login del usuario
def login(request):
    username= request.POST['username']
    password= request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('SGIAPP:userilist'))
        else:
            return render(request,'SGIAPP/home.html', {'error':"Cuenta desactivada"})
    else:
        return render(request,'SGIAPP/home.html', {'error':"Nombre de usuario o contraseña incorrectas"})

# Muestra un formulario para crear un nuevo usuario
def register(request):
    return render(request,'SGIAPP/register.html',{})

# Procesa la creación de usuarios
def doregistration(request):
    username= request.POST['username']
    password= request.POST['password']
    cpassword= request.POST['cpassword']
    email = request.POST['email']

    if password==cpassword:
        try:
            validate_email(email)
        except ValidationError:
            return render(request,'SGIAPP/register.html',{'error':'Inserte una dirección de correo válida'})
        User.objects.create_user(username, email, password)
        user = authenticate(username=username, password=password)
        auth.login(request, user)
        return HttpResponseRedirect(reverse('SGIAPP:userilist'))
    else:
        return render(request,'SGIAPP/register.html',{'error':'Las contraseñas no coinciden'})

# Procesa la desconexión e imprime un mensaje de éxito
def logout(request):
    auth.logout(request)
    return render(request,'SGIAPP/logout.html')

# Lista las incidencias reportadas por el usuario, desde aquí
# puede revisar el estado de las mismas y acceder a sus detalles
def userilist(request):
    object_list= Incidence.objects.filter(notifier__username__exact= request.user.username)\
    .order_by('-pub_date')
    related_entities= Entity.objects.filter(users=request.user)
    entity_assoc= False
    if related_entities:
        entity_assoc=True
    return render(request,'SGIAPP/incidences_listing.html',\
        {'user':request.user, 'object_list': object_list, 'entities':entity_assoc})

# Para mostrar los detalles de una Incidencia
class IncidencesDetailView(DetailView):
    model = Incidence
    template_name = 'SGIAPP/incidences_detail.html'

# Muestra un form para reportar una incidencia
def incidence_report(request):
    entities= Entity.objects.all()
    return render(request,'SGIAPP/report_incidence.html',{'entities':entities})

# Procesa el form de reportar incidencias
def do_report(request):
    content=request.POST['content']
    entityid=request.POST['entity']
    entity= Entity.objects.get(id=entityid)
    user= request.user
    date= datetime.now()
    i= Incidence(content=content,pub_date=date,notifier=user,entity=entity)
    i.save()
    return HttpResponseRedirect(reverse('SGIAPP:userilist'))

# Muestra un listado de las inicidencias asociadas a la entidad a
# la que pertenece el usuario, si este perteneciera a alguna
# y le permite modificar el estado de las incidencias
def check_for_entity_incidences(request):
    user=request.user
    related_entities= Entity.objects.filter(users=user)
    entities= Incidence.objects.filter(entity=related_entities).order_by('-pub_date')
    return render(request,'SGIAPP/check_incidences.html',{'object_list':entities})

# Procesa la confirmación de una incidencia
def confirm(request, id):
    i=Incidence.objects.get(id=id)
    i.confirmed=True
    i.confirmation_date=datetime.now()
    i.save()
    return HttpResponseRedirect(reverse('SGIAPP:check_incidences'))

# Muestra un form para poner el mensaje de finalización
def finish(request, id):
    return render(request,'SGIAPP/fill_finish_message.html',{'id':id})

# Procesa la finalización de la incidencia
def do_finish(request):
    id= request.POST['id']
    finishmsg= request.POST['content']
    i=Incidence.objects.get(id=id)
    i.finished=True
    i.finishing_date= datetime.now()
    i.finished_msg=finishmsg
    i.save()
    return HttpResponseRedirect(reverse('SGIAPP:check_incidences'))

    return HttpResponseRedirect(reverse('SGIAPP:check_incidences'))