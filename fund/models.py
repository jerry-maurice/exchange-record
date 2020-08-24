from django.db import models
from country.models import Country
from company.models import Company

# Create your models here.
class Fund(models.Model):
    '''
    account holder will be able to view how  much  fund they have available
    This object will be  use as a safe
    '''
    funds = models.FloatField(null=False, default=0.00)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='country_fund')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_fund')
        
    def __str__(self):
        return f'{self.funds}. {self.country.name}'


class FundTransaction(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    deposited = models.FloatField(null=False, default=0.0)
    withdrew = models.FloatField(null=False, default=0.0)
    previous_balance = models.FloatField(null=False, default=0.0)
    actual_balance = models.FloatField(null=False, default=0.0)
    source = models.CharField(null=True, max_length=500)       # source of income
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE, related_name='transaction_fund')
    comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('-created',)
        
    def __str__(self):
        return f'{self.created}. {self.previous_balance}. {self.actual_balance}'