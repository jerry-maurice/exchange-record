from django.db import models

# Create your models here.
class Plan(models.Model):
    '''
    List of all  plan and their description
    '''
    name = models.CharField(null=False, max_length=500)
    description = models.TextField(null=False)
    employee = models.PositiveIntegerField(null=False)
    price = models.FloatField(null=False)

    class Meta:
        ordering = ('name',)
        
    def __str__(self):
        return self.name
