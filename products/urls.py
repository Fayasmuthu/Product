from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = "products"

urlpatterns = [
 
    path("", views.shop, name="products"),
    path('test',views.Product.as_view(), name='test'),
    path('category',views.CategorysView.as_view(),name='category'),

    path('subcategory',views.SubsCategoryView.as_view(),name='subcategory')


    # path("about/", TemplateView.as_view(template_name="web/about.html")),
    # path("contact/", views.contact, name="contact"),
]