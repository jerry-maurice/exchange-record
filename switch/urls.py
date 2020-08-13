"""switch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404,  handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',  include('overview.urls')),
    path('authenticate/',  include('authentication.urls')),
    path('employee/',  include('employee.urls')),
    path('clients/',  include('client.urls')),
    path('country/',  include('country.urls')),
    path('register/',  include('register.urls')),
    path('sale/',  include('sale.urls')),
    path('support/',  include('support.urls')),
    path('account/',  include('account.urls')),
]
handler404 = 'employee.views.handler404'
handler500 = 'employee.views.handler505'