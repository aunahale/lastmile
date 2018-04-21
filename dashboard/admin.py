from django.contrib import admin

# Register your models here.
from .models import Distributor
from .models import Retailer
from .models import Item
from .models import Order_item
from .models import Order_summary
from .models import Van
from .models import User_assignment

admin.site.register(Distributor)
admin.site.register(Retailer)
admin.site.register(Item)
admin.site.register(Order_item)
admin.site.register(Order_summary)
admin.site.register(Van)
admin.site.register(User_assignment)
