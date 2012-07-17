from django.db import models
from django.contrib.auth.models import User

class NameList(models.Model):
    title = models.CharField(max_length=50)
    user = models.ForeignKey(User, blank=True, null=True)
    def __unicode__(self):
        return self.title
    
class Person(models.Model):
    name = models.CharField(max_length=50, unique=True)
    namelist = models.ForeignKey(NameList, related_name='people')
    forbidden_pairings = models.ManyToManyField("self")
    
    def __unicode__(self):
        return self.name
    
class Pairing(models.Model):
    people = models.ManyToManyField(Person, related_name='pairings')
    count = models.IntegerField(default=0)
    last_pairing = models.DateTimeField(auto_now=True)
    namelist = models.ForeignKey(NameList, related_name='pairings')
    
    def __unicode__(self):
        return ', '.join([person.name for person in self.people.all()])
        
class Groups(models.Model):
    namelist = models.ForeignKey(NameList)
    name = models.CharField(max_length=20, blank=True, null=True)
    people = models.ManyToManyField(Person, blank=True, null=True)
    date = models.DateTimeField(auto_now=True)