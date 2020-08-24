from django.db import models
from company.models import Company

# Create your models here.
class Country(models.Model):
    '''
    list of country available in the app
    '''
    name = models.CharField(null=False, max_length=250)
    alpha2Code = models.CharField(null=False, max_length=2)
    alpha3Code = models.CharField(null=False, max_length=3)
    currency = models.CharField(null=False, max_length=100)
    flag = models.CharField(null=True, max_length=500)
    language = models.CharField(null=False, max_length=250)
    company = models.ForeignKey(Company,  on_delete = models.CASCADE, related_name='country_company')

    class Meta:
        ordering = ('name',)
        verbose_name = 'country'
        verbose_name_plural = 'countries'

    def __str__(self):
        return self.name