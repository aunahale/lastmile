from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Order_sku(models.Model):
    shop_Id = models.PositiveIntegerField()
    sku = models.CharField(max_length=20)

    def __str__(self):
        return str(self.shop_Id)+' '+self.sku


class Distributor(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Retailer(models.Model):
    shop_id = models.CharField(max_length=100)
    distributor = models.ForeignKey(Distributor, on_delete = models.CASCADE)
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('shop_id', 'distributor'),)

class Facility(models.Model):
    name = models.CharField(max_length=100)
    facility_id = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    distributor = models.ForeignKey(Distributor, on_delete = models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()

class Van(models.Model):
    distributor = models.ForeignKey(Distributor, on_delete = models.CASCADE)
    van_id = models.CharField(max_length=100)
    capacity_vol = models.FloatField()
    capacity_weight = models.FloatField()
    rate_per_mile = models.FloatField()
    fixed_cost = models.FloatField()
    speed = models.FloatField()

class Item(models.Model):
    distributor = models.ForeignKey(Distributor, on_delete = models.CASCADE)
    item_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    weight = models.FloatField()
    volume = models.FloatField()


class Order_item(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete = models.CASCADE)
    order_id = models.CharField(max_length=100)
    date =  models.DateField()
    item = models.ForeignKey(Item, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField()

class Order_summary(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete = models.CASCADE)
    order_id =  models.CharField(max_length=100)
    date =  models.DateField()
    quantity_sum = models.PositiveIntegerField()
    weight_sum = models.FloatField()
    vol_sum = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()

class Route(models.Model):
    date =  models.DateField()
    sequence = models.PositiveIntegerField()
    order_id =  models.CharField(max_length=100)
    sum_unique_item = models.PositiveIntegerField()
    sum_quantity = models.PositiveIntegerField()
    van = models.ForeignKey(Van, on_delete = models.CASCADE)


class Pick(models.Model):
    date =  models.DateField()
    route = models.ForeignKey(Route, on_delete = models.CASCADE)
    order_id =  models.CharField(max_length=100)
    item = models.ForeignKey(Item, on_delete = models.CASCADE)
    item_quantity = models.PositiveIntegerField()
    van = models.ForeignKey(Van, on_delete = models.CASCADE)

class User_assignment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    distributor = models.ForeignKey(Distributor, on_delete = models.CASCADE)
