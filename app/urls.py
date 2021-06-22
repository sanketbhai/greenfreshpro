from django.urls import path
from .views import *
urlpatterns = [
    path('',home,name='home'),
    path('signin/',index,name='signin'),
    path('signup/',signup,name='signup'),
    path('cart/',cart,name='cart'),
    path('logout/',logout,name='logout'),
    path('gotocart/',gotocart,name='gotocart'),
    path('contactus/',contactus,name='contactus'),
    path('order/',order,name='order'),
path('payment/',payment,name='payment'),


    ]
