from django.contrib import admin
from django.urls import path, include

from venta import views


urlpatterns = [
    path('productos/', views.productos, name='productos'),
    path('productos/add/', views.producto_add, name='producto_add'),
    path('productos/<int:id_p>/', views.producto_edit, name='producto_edit'),
    path('productos/<int:id_p>/del/', views.producto_del, name='producto_del'),
    path('pedidos/', views.pedidos, name='pedidos'),
    path('pedidos/add/', views.pedido_add, name='pedido_add'),
    path('pedido/<int:id_p>/', views.pedido_edit, name='pedido_edit'),
    path('pedido/<int:id_p>/del/', views.pedido_del, name='pedido_del'),
    path('pedido/<int:id_p>/add/', views.item_add, name='item_add'),
    path('pedido/<int:id_p>/del/<int:id_i>', views.item_del, name='item_del'),
]