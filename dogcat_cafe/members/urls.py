from django.urls import path
from members.views import *

urlpatterns = [
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("foods/", food_list, name="foods"),
    path('calendar-events/', CalendarEvents.as_view(), name='calendar_events'),
    path('pets/<int:id>/',pets, name='pets'),
    path('dashborad/',dashboard, name='dashboard'),
    path('cart/', cart_detail, name='cart_detail'),
    path('add_to_cart/<int:food_id>/', add_to_cart, name='add_to_cart'),
    path('decrease_quantity/<int:food_id>/', decrease_quantity, name='decrease_quantity'),
    path('increase_quantity/<int:food_id>/', increase_quantity, name='increase_quantity'),
    path('remove_from_cart/<int:food_id>/', remove_from_cart, name='remove_from_cart'),
    path('create_order/', create_order, name='create_order'),
    path('order/', order_detail, name='order'),
    path('send_order_email/', send_order_email, name='send_order_email'),
    path('order_history/', order_history, name='order_history'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    ]

