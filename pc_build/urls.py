from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('build/', views.build),
    path('build/addpart/<part_id>/', views.add_part_build),
    path('build/removepart/<part_id>/', views.remove_part_build),
    path('orders/', views.orders),
    path('orders/<order_id>/', views.order_info),
    path('shop/', views.shop),
    path('shop/addpart/<part_id>/', views.add_part_shop),
    path('shop/removepart/<part_id>/', views.remove_part_shop),
    path('checkout/', views.checkout),
    path('cart/', views.cart),
    path('scrape/<part_type>/<pages>/', views.scrape),
]