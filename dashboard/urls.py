from . import views
from django.urls import path

app_name = 'dashboard'

urlpatterns = [

    #/dashboard/
    path('', views.index, name='index'),
]
