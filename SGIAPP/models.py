from django.db import models
from django.contrib.auth.models import User

# El la clase User viene como parte del framework

# Este es la clase que representa las entidades a las que se le reportan
# las incidencias, hay usuarios asociados a estas entidades que se encargan
# de procesar el manejo de las incidencias, es decir confirmarlas y cuando se
# resuelvan fianlizarlas y dar un mensaje
class Entity(models.Model):
    name= models.CharField(max_length=50)
    description= models.TextField()
    address = models.CharField(max_length=75)
    phone = models.CharField(max_length=30)
    email= models.EmailField(max_length=30)
    users= models.ManyToManyField(User)
    users.null=True

    def __unicode__(self): #para modificar como se imprime el objeto
        return self.name

# Representa una incidencia en el sistema, con un contenido,....y un notificador
# que es un User y entidad a la que se reporta que es una de las Entity de arriba
class Incidence(models.Model):
    content= models.TextField()

    confirmed= models.BooleanField()

    finished= models.BooleanField()

    pub_date= models.DateTimeField()

    confirmation_date= models.DateTimeField()
    confirmation_date.null=True

    finishing_date= models.DateTimeField()
    finishing_date.null=True

    finished_msg = models.TextField()
    finished_msg.null= True

    notifier= models.ForeignKey(User)

    entity= models.ForeignKey(Entity)
    def __unicode__(self):
        return self.content