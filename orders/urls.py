from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = "orders"

urlpatterns = [
    # path("", views.index, name="index"),
    # path("about/", TemplateView.as_view(template_name="web/about.html")),
    # path("contact/", views.contact, name="contact"),
]