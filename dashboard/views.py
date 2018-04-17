from django.http import Http404,HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Order_sku
import random

# Create your views here.

def index(request):
    randomID = random.randint(1,101)
    a = Order_sku(shopId=randomID,sku = 'qfawe' )

    a.save()
    return HttpResponse("<p>test</p>")
'''
    all_albums = Album.objects.all()

    context = {
    'all_albums': all_albums,
    }
    return render(request, 'music/index.html',context)
'''
