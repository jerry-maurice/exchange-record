from django.db import models
from company.models import Company

# Create your models here.
class Client(models.Model):
    picture = models.URLField(null=True)
    identification  = models.CharField(null=True, max_length=250)
    first_name = models.CharField(null=False, max_length=250)
    last_name = models.CharField(null=False, max_length=250)
    email = models.EmailField(null=True)
    gender = models.CharField(null=True, max_length=50)
    dob = models.DateField(null=True)
    phone = models.CharField(max_length=20, null=False)
    created = models.DateField(auto_now_add=True, null=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='client_company')

    class Meta:
        ordering = ('first_name',)

    def __str__(self):
        return self.first_name +" "+ self.last_name