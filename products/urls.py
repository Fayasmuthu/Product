from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = "products"

urlpatterns = [
    path("", views.home, name="index"),
    path("products", views.shop, name="products"),
    path('test',views.Product.as_view(), name='test'),
    path('category',views.CategorysView.as_view(),name='category'),
    path('subcategory',views.SubsCategoryView.as_view(),name='subcategory'),
    path('details/<slug:slug>/',views.products_detailsViews.as_view(),name='products_details'),

    #Account
    path('myaccount',views.myaccount, name="myaccount"),

    #Cart
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
    path('cart/cart-update/', views.update_cart_quantity, name='update_cart_quantity'),
    path('cart/checkout/', views.checkout, name='checkout'),

]