from . import views
from django.urls import path

app_name = 'dashboard'

urlpatterns = [

    #/dashboard/
    path('', views.index, name='index'),
    path('order', views.order, name='order'),
    path('order_add', views.order_add, name='order_add'),
    path('order_submit', views.order_submit, name='order_submit'),
    path('order_detail/<str:order_date>', views.order_detail, name='order_detail'),
    path('shop', views.shop, name='shop'),
    path('shop_add', views.shop_add, name='shop_add'),
    path('shop_submit', views.shop_submit, name='shop_submit'),
    path('shop_edit/<int:store_pk>/',views.shop_edit, name='shop_edit'),
    path('shop_detail/<int:store_pk>/',views.shop_detail, name='shop_detail'),
    path('shop_delete/<int:store_pk>/',views.shop_delete, name='shop_delete'),
    path('shop_search', views.shop_search, name='shop_search'),
    path('user', views.user, name='user'),
    path('user_edit', views.user_edit, name='user_edit'),
    path('user_submit', views.user_submit, name='user_submit'),
    path('resource', views.resource, name='resource'),
    path('truck_add', views.truck_add, name='truck_add'),
    path('truck_submit', views.truck_submit, name='truck_submit'),
    path('truck_edit/<int:truck_pk>/',views.truck_edit, name='truck_edit'),
    path('truck_delete/<int:truck_pk>/',views.truck_delete, name='truck_delete'),
    path('facility_add', views.facility_add, name='facility_add'),
    path('facility_edit/<int:facility_pk>/',views.facility_edit, name='facility_edit'),
    path('facility_delete/<int:facility_pk>/',views.facility_delete, name='facility_delete'),
    path('facility_submit', views.facility_submit, name='facility_submit'),
    path('item_add', views.item_add, name='item_add'),
    path('item_edit/<int:item_pk>/',views.item_edit, name='item_edit'),
    path('item_detail/<int:item_pk>/',views.item_detail, name='item_detail'),
    path('item_submit', views.item_submit, name='item_submit'),
    path('item_delete/<int:item_pk>/',views.item_delete, name='item_delete'),
    path('item', views.item, name='item'),
    path('register',views.register,name="register"),
    path('register_submt',views.register_submit,name="register_submit"),
    path('login',views.login_page,name="login"),
    path('login_submit',views.login_submit,name="login_submit"),
    path('logout',views.logout_view,name="logout"),
    #path('register', views.UserFormView.as_view(), name='register')
]
