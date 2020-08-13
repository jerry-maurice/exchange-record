from django.contrib import admin
from register.models import Register,  Register_Log,  Register_Status, RegisterAssigned

# Register your models here.
admin.site.register(Register)
admin.site.register(Register_Log)
admin.site.register(Register_Status)
admin.site.register(RegisterAssigned)
