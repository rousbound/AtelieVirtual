from django.db import models
import json
import os

# Create your models here.
class PL(models.Model):
    project = models.CharField(max_length=256)
    ementa = models.CharField(max_length=2046)
    localdata = models.CharField(max_length=128, null=True, default= "Governador")
    sessiondate = models.CharField(max_length=128)
    
    def jsonToClass(self, jsonDict):
        self.project = jsonDict['projeto']
        self.ementa = jsonDict['ementa']
        self.localdata = jsonDict['localdata']
        self.sessiondate = jsonDict['session_date']

def createObjectsFromJson(path):
    with open(path, "r") as fp:
        json_data = json.load(fp)
        print(json_data)
        for pl in json_data:
            plObject, created = PL.objects.get_or_create(project = pl['projeto'])
            if created:
                plObject.jsonToClass(pl)
                plObject.save()
            else:
                plObject.update(sessiondate = pl['session_date'])
                plObject.update(ementa = pl['ementa'])




