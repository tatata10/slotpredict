from django.db import models
from datetime import date

# Create your models here.
class data(models.Model):
    storeName = models.CharField(max_length=100,default="0")
    date = models.DateField(default=date(1111, 1, 1))
    modelName = models.CharField(max_length=100)
    number = models.IntegerField(default=0)
    game = models.IntegerField(default=0)
    difference = models.IntegerField(default=0)
    BB = models.IntegerField(default=0)
    RB = models.IntegerField(default=0)
    allprobability = models.FloatField(default=0.0)
    BBprobability = models.FloatField(default=0.0)
    RBprobability = models.FloatField(default=0.0)
    setting = models.IntegerField(default=0)
# =============================================================================
# class data(models.Model):
#     modelName = models.CharField(max_length=100)
#     number = models.CharField(max_length=100)
#     game = models.CharField(max_length=100)
#     difference = models.CharField(max_length=100)
#     BB = models.CharField(max_length=100)
#     RB = models.CharField(max_length=100)
#     full = models.CharField(max_length=100)
#     BBprobability = models.CharField(max_length=100)
#     RBprobability = models.CharField(max_length=100)
# =============================================================================

class Friend(models.Model):
    name = models.CharField(max_length=100)
    mail = models.EmailField(max_length=200)
    gender = models.BooleanField()
    age = models.IntegerField(default=0)
    birthday = models.DateField()
    
    def __str__(self):
        return '<Frinend:id' + str(self.id) + ',' + \
            self.name + '(' + str(self.age) +')>'
            
class standard_data(models.Model):
    level = models.IntegerField(default=0)
    modelName = models.CharField(max_length=100)
    allprobability = models.FloatField(default=0.0)
    BBprobability = models.FloatField(default=0.0)
    RBprobability = models.FloatField(default=0.0)
            

