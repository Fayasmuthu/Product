from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = "main"

urlpatterns = [
    # path("", views.products, name="products"),
    # path("/", TemplateView.as_view(template_name="web/about.html")),
    # path("contact/", views.contact, name="contact"),
]