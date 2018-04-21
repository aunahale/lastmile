from django.http import Http404,HttpResponse
from django.shortcuts import render, get_object_or_404,redirect
from .models import Order_sku
from .models import Distributor, Retailer, Item, Order_item, Order_summary,Van, Facility, User_assignment
from django.db.models import Count,Sum,F,FloatField
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

import random


# Create your views here.
class UserFormView(View):
    form_class = UserForm
    template_name = 'registration_form.html'

    def get(self,request):
        form = self.form_class(None)
        return render(request,self.template_name, {'form':form})

    def post(self,request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user.set_password(password)
            user.save()

            user = authenticate(username=username,password=password)

            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect("dashboard:user")

        return render(request,self.template_name, {'form':form})





def register(request):
    return render(request,'register.html')

def register_submit(request):

     if request.method == "GET":
         return redirect("dashboard:register")


     username = request.POST['username']
     password = request.POST['password']


     user = User()
     user.username = username
     user.set_password(password)
     user.save()

     name = request.POST['dist_name']
     number = request.POST['number']
     address1 = request.POST['address1']
     address2 = request.POST['address2']
     city = request.POST['city']
     state = request.POST['state']
     dbr = Distributor(name=name, number=number, address1=address1, city=city, state=state)
     dbr.save()

     user_assign = User_assignment(user = user, distributor=dbr)
     user_assign.save()

     user = authenticate(username=username,password=password)
     login(request,user)

     return redirect("dashboard:user")


def login_page(request):
    return render(request, 'login.html')

def login_submit(request):

    if request.method == "GET":
        return redirect("dashboard:login")

    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username,password=password)
    login(request,user)
    return redirect("dashboard:user")

def logout_view(request):
    logout(request)
    return redirect("dashboard:login")

def index(request):
    randomID = random.randint(1,101)
    a = Order_sku(shopId=randomID,sku = 'qfawe' )

    a.save()
    return HttpResponse("<p>test</p>")

@login_required(login_url='dashboard:login')
def order(request):

    user = request.user.username
    user = User_assignment.objects.filter(user__username=user)
    dbr = user[0].distributor

    summary = Order_summary.objects.filter(retailer__distributor=dbr).values('date').annotate(shop_number = Count('retailer'),quantity_total = Sum('quantity_sum')).order_by('date')
    display_length = min(3,len(summary))
    summary = summary[0:display_length]
    #summary = Order_summary.objects.get(pk=1)
    return render(request, 'order.html',{'summary':summary})

@login_required(login_url='dashboard:login')
def order_add(request):
    return render(request, 'order_add.html')

@login_required(login_url='dashboard:login')
def order_submit(request):


        if request.method == "GET":
            return redirect("dashboard:order")

        date = request.POST['date']


        user = request.user.username
        user = User_assignment.objects.filter(user__username=user)
        dbr = user[0].distributor


        try:

            csv_file = request.FILES["csv_file"]
            line = csv_file.readlines()
            i = 0
            index = -1
            for row in line:
                s = str(row)
                s = s[2:(s.find("\\")-len(s))]
                d = s.split(",")
                if i==0:
                    i=1
                    try:
                        retail_index = d.index('shopId')
                        order_id_index = d.index('orderId')
                        item_index = d.index('itemId')
                        quantity_index = d.index('quantity')
                    except:
                        raise Http404("Some Fields are Missing!")
                else:
                    retailId = d[retail_index]
                    orderId = d[order_id_index]
                    itemId = d[item_index]
                    quantity = d[quantity_index]

                    rtl = Retailer.objects.get(distributor = dbr, shop_id = retailId)
                    item = Item.objects.get(distributor = dbr, item_id = itemId)
                    orderItem = Order_item(retailer = rtl, order_id = orderId, date = date, item = item, quantity = quantity)
                    orderItem.save()

            qry = Order_item.objects.values('retailer','order_id','date','retailer__latitude','retailer__longitude').annotate(qty_sum = Sum('quantity'),vol_sum = Sum(F('quantity')*F('item__volume'),output_field=FloatField()),weight_sum = Sum(F('quantity')*F('item__weight'),output_field=FloatField()))

            for result in qry:
                order_summary = Order_summary()
                order_summary.retailer = Retailer.objects.get(pk = result['retailer'])
                order_summary.order_id = result['order_id']
                order_summary.date = result['date']
                order_summary.quantity_sum = result['qty_sum']
                order_summary.weight_sum = result['weight_sum']
                order_summary.vol_sum =  result['vol_sum']
                order_summary.latitude = result['retailer__latitude']
                order_summary.longitude = result['retailer__longitude']
                order_summary.save()





            return HttpResponse("<p>asdf</p>")

        except Exception as e:
            return HttpResponse("<p>"+str(e)+"</p>")


@login_required(login_url='dashboard:login')
def shop(request):

        user = request.user.username
        user = User_assignment.objects.filter(user__username=user)
        dbr = user[0].distributor

        retailer_list = Retailer.objects.filter(distributor=dbr)

        paginator = Paginator(retailer_list, 1) # Show 25 contacts per page

        page = request.GET.get('page')
        retailer = paginator.get_page(page)

        return render(request, 'shop.html', {'retailer': retailer})


@login_required(login_url='dashboard:login')
def shop_add(request):
    return render(request, 'shop_add.html')

@login_required(login_url='dashboard:login')
def shop_search(request):
    shop_id = request.POST['shop_id']
    retail = Retailer.objects.get(shop_id=shop_id)
    pk = retail.pk
    return redirect("./shop_detail/"+str(pk))

@login_required(login_url='dashboard:login')
def shop_submit(request):

    if request.method == "GET":
        return redirect("dashboard:shop")

    else:
        user = request.user.username
        user = User_assignment.objects.filter(user__username=user)
        dbr = user[0].distributor

        submit_type = request.POST['submit_type']
        if submit_type!="0": #fill form

            shop_id = request.POST['shop_id']
            name = request.POST['shop_name']
            number = request.POST['number']
            address1 = request.POST['address1']
            address2 = request.POST['address2']
            city = request.POST['city']
            state = request.POST['state']
            latitude = request.POST['latitude']
            longitude = request.POST['longitude']

            if submit_type=="1":
                retailer = Retailer(shop_id=shop_id, distributor=dbr, name=name, number=number, address1=address1, address2=address2,city=city,state=state, latitude=latitude, longitude=longitude)
                retailer.save()
            else:
                Retailer.objects.filter(pk = request.POST['pk']).update(shop_id=shop_id, distributor=dbr, name=name, number=number, address1=address1, address2=address2,city=city,state=state, latitude=latitude, longitude=longitude)
                return redirect("./shop_detail/"+str(request.POST['pk']))
        else:

            try:

                csv_file = request.FILES["csv_file"]
                line = csv_file.readlines()
                i = 0
                index = -1
                for row in line:
                    s = str(row)
                    s = s[2:(s.find("\\")-len(s))]
                    d = s.split(",")
                    if i==0:
                        i=1
                        try:

                            shop_id_index = d.index('shopId')
                            name_index = d.index('name')
                            number_index = d.index('number')
                            address1_index = d.index('address1')
                            address2_index = d.index('address2')
                            city_index = d.index('city')
                            state_index = d.index('state')
                            latitude_index = d.index('latitude')
                            longitude_index = d.index('longitude')

                        except:
                            raise Http404("Some Fields are Missing!")
                    else:
                        shop_id =d[shop_id_index]
                        name = d[name_index]
                        number = d[number_index]
                        address1 = d[address1_index]
                        address2 = d[address2_index]
                        city = d[city_index]
                        state = d[state_index]
                        latitude = d[latitude_index]
                        longitude = d[longitude_index]

                        retailer = Retailer(shop_id=shop_id, distributor=dbr, name=name, number=number, address1=address1, address2=address2,city=city,state=state, latitude=latitude, longitude=longitude)
                        retailer.save()



                return redirect("dashboard:shop")

            except Exception as e:
                return HttpResponse("<p>"+str(e)+"</p>")




    return HttpResponse("<p>asdf</p>")

@login_required(login_url='dashboard:login')
def shop_delete(request, store_pk):

    user = request.user.username
    user = User_assignment.objects.filter(user__username=user)
    dbr = user[0].distributor


    retailer = Retailer.objects.get(pk=store_pk)

    if retailer.distributor!=dbr:
        return HttpResponse("<p>You don't have the permission to view this page<p>")

    retailer.delete()

    return redirect("./resource")

@login_required(login_url='dashboard:login')
def shop_edit(request, store_pk):

    user = request.user.username
    user = User_assignment.objects.filter(user__username=user)
    dbr = user[0].distributor
    shop = Retailer.objects.get(pk=store_pk)

    if shop.distributor!=dbr:
        return HttpResponse("<p>asdf</p>")

    return render(request, 'shop_edit.html',{'shop':shop})

@login_required(login_url='dashboard:login')
def shop_detail(request, store_pk):

    user = request.user.username
    user = User_assignment.objects.filter(user__username=user)
    dbr = user[0].distributor

    shop = Retailer.objects.get(pk=store_pk)
    if shop.distributor!=dbr:
        return HttpResponse("<p>You don't have the permission to view this page</p>")

    return render(request, 'shop_detail.html',{'shop':shop})

@login_required(login_url='dashboard:login')
def user(request):


    user = request.user.username
    user = User_assignment.objects.filter(user__username=user)
    dbr = user[0].distributor

    #dbr = Distributor.objects.get(pk=1)
    return render(request,'distributor_profile.html',{'distributor':dbr})

@login_required(login_url='dashboard:login')
def user_edit(request):
    user = request.user.username
    user = User_assignment.objects.filter(user__username=user)
    dbr = user[0].distributor
    return render(request, 'distributor_edit.html',{'distributor':dbr})

@login_required(login_url='dashboard:login')
def user_submit(request):

    if request.method == "GET":
        return redirect("dashboard:user")

    else:
        name = request.POST['dist_name']
        number = request.POST['number']
        address1 = request.POST['address1']
        address2 = request.POST['address2']
        city = request.POST['city']
        state = request.POST['state']
        Distributor.objects.filter(pk = request.POST['pk']).update(name=name, number=number, address1=address1, city=city, state=state)

        return redirect("./user")

@login_required(login_url='dashboard:login')
def resource(request):
    user = request.user.username
    user = User_assignment.objects.filter(user__username=user)
    dbr = user[0].distributor
    facility = Facility.objects.filter(distributor=dbr)
    truck = Van.objects.filter(distributor=dbr)


    return render(request, 'resource.html', {'facility':facility,'truck':truck})

@login_required(login_url='dashboard:login')
def truck_add(request):
    return render(request, 'truck_add.html')

@login_required(login_url='dashboard:login')
def truck_submit(request):

    if request.method == "GET":
        return redirect("dashboard:resource")

    else:
        user = request.user.username
        user = User_assignment.objects.filter(user__username=user)
        dbr = user[0].distributor
        id = request.POST['id']
        volume_capacity = request.POST['volume_capacity']
        weight_capacity = request.POST['weight_capacity']
        rate = request.POST['rate']
        fixed_cost = request.POST['fixed_cost']
        speed = request.POST['speed']

        if request.POST['submit_type']=="0":

            van = Van(distributor=dbr,van_id=id, capacity_vol=volume_capacity,capacity_weight=weight_capacity,rate_per_mile=rate,fixed_cost=fixed_cost,speed=speed)
            van.save()
        else:

            Van.objects.filter(pk = request.POST['pk']).update(distributor=dbr,id=id, capacity_vol=volume_capacity,capacity_weight=weight_capacity,rate_per_mile=rate,fixed_cost=fixed_cost,speed=speed)

        return redirect("./resource")

@login_required(login_url='dashboard:login')
def truck_edit(request, truck_pk):
    van = Van.objects.get(pk=truck_pk)

    return render(request, 'truck_edit.html',{'van':van})

@login_required(login_url='dashboard:login')
def truck_delete(request, truck_pk):
    Van.objects.get(pk=truck_pk).delete()

    return redirect("./resource")

@login_required(login_url='dashboard:login')
def facility_add(request):
    return render(request, 'facility_add.html')

@login_required(login_url='dashboard:login')
def facility_submit(request):

    if request.method == "GET":
        return redirect("dashboard:resource")

    user = request.user.username
    user = User_assignment.objects.filter(user__username=user)
    dbr = user[0].distributor

    facility_id = request.POST['facility_id']
    name = request.POST['facility_name']
    number = request.POST['number']
    address1 = request.POST['address1']
    address2 = request.POST['address2']
    city = request.POST['city']
    state = request.POST['state']
    latitude = request.POST['latitude']
    longitude = request.POST['longitude']

    if request.POST['submit_type']=="0":

        facility = Facility(facility_id=facility_id, distributor=dbr, name=name, number=number, address1=address1, address2=address2,city=city,state=state, latitude=latitude, longitude=longitude)
        facility.save()
    else:

        Facility.objects.filter(pk = request.POST['pk']).update(facility_id=facility_id, distributor=dbr, name=name, number=number, address1=address1, address2=address2,city=city,state=state, latitude=latitude, longitude=longitude)

    return redirect("./resource")

@login_required(login_url='dashboard:login')
def facility_edit(request, facility_pk):
    facility = Facility.objects.get(pk=facility_pk)
    return render(request, 'facility_edit.html',{'facility':facility})

@login_required(login_url='dashboard:login')
def facility_delete(request, facility_pk):
    Facility.objects.get(pk=facility_pk).delete()
    return redirect("./resource")

@login_required(login_url='dashboard:login')
def item_add(request):
    return render(request, 'item_add.html')

@login_required(login_url='dashboard:login')
def item_submit(request):


    if request.method == "GET":
        return redirect("dashboard:item")


    user = request.user.username
    user = User_assignment.objects.filter(user__username=user)
    dbr = user[0].distributor

    submit_type = request.POST['submit_type']
    if submit_type!="0": #fill form

        item_id = request.POST['item_id']
        name = request.POST['item_name']
        weight = request.POST['weight']
        volume = request.POST['volume']

        if submit_type=="1":
            item = Item(item_id=item_id, distributor=dbr, name=name, weight=weight, volume=volume)
            item.save()
        else:
            Item.objects.filter(pk = request.POST['pk']).update(item_id=item_id, distributor=dbr, name=name, weight=weight, volume=volume)
            return redirect("./item_detail/"+str(request.POST['pk']))

    else:

        try:

            csv_file = request.FILES["csv_file"]
            line = csv_file.readlines()
            i = 0
            index = -1
            for row in line:
                s = str(row)
                s = s[2:(s.find("\\")-len(s))]
                d = s.split(",")
                if i==0:
                    i=1
                    try:

                        item_id_index = d.index('itemId')
                        name_index = d.index('name')
                        weight_index = d.index('weight')
                        volume_index = d.index('volume')


                    except:
                        raise Http404("Some Fields are Missing!")
                else:
                    item_id =d[item_id_index]
                    name = d[name_index]
                    weight = d[weight_index]
                    volume = d[volume_index]

                    item =Item(item_id=item_id, distributor=dbr, name=name, weight=weight, volume=volume)
                    item.save()



            return HttpResponse("<p>asdf</p>")

        except Exception as e:
            return HttpResponse("<p>"+str(e)+"</p>")




    return HttpResponse("<p>asdf</p>")

@login_required(login_url='dashboard:login')
def item_edit(request, item_pk):
    item = Item.objects.get(pk=item_pk)
    return render(request, 'item_edit.html',{'item':item})

@login_required(login_url='dashboard:login')
def item_delete(request, item_pk):
    Item.objects.get(pk=item_pk).delete()
    return redirect("./item")

@login_required(login_url='dashboard:login')
def item(request):

        user = request.user.username
        user = User_assignment.objects.filter(user__username=user)
        dbr = user[0].distributor


        item_list =Item.objects.filter(distributor = dbr)

        paginator = Paginator(item_list, 1) # Show 25 contacts per page

        page = request.GET.get('page')
        item = paginator.get_page(page)

        return render(request, 'item.html', {'item': item})

@login_required(login_url='dashboard:login')
def item_detail(request, item_pk):

    user = request.user.username
    user = User_assignment.objects.filter(user__username=user)
    dbr = user[0].distributor
    item = Item.objects.get(pk=item_pk)
    if item.distributor!=dbr:
        return HttpResponse("<p>You don't have the permission to view this page</p>")

    return render(request, 'item_detail.html',{'item':item})

@login_required(login_url='dashboard:login')
def order_detail(request,order_date):

    user = request.user.username
    user = User_assignment.objects.filter(user__username=user)
    dbr = user[0].distributor

    order = Order_summary.objects.filter(date=order_date,retailer__distributor = dbr)

    order_date = order[0].date

    return render(request, 'order_detail.html',{'order':order,'date':order_date})
