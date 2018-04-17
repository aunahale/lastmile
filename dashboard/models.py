from django.db import models

# Create your models here.
class Order_sku(models.Model):
    shopId = models.PositiveIntegerField()
    sku = models.CharField(max_length=20)

    def __str__(self):
        return str(self.shopId)+' '+self.sku
