from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView ,TemplateView 
from django.views.generic.edit import FormView
from .models import Product ,Categorys,SubsCategory
 
# Create your views here.

class Product(ListView):
    model = Product 
    template_name = 'products/test.html'
    context_object_name = 'products'






    # subcategory_id = request.GET.get('subcategory')
    # if subcategory_id:
    #     selected_subcategory = SubsCategory.objects.get(pk=subcategory_id)
    #     products = Product1.objects.filter(SubsCategory=selected_subcategory)

    # if subcategory_id:
    #     selected_subcategory = SubsCategory.objects.get(pk=subcategory_id)
    #     products = Product1.objects.filter(SubsCategory=selected_subcategory)
    # else:
    #     products = Product1.objects.all()
   
    # products_on_sale = [product for product in products if product.is_on_sale()]

class CategorysView(ListView):
    model = Categorys 
    template_name = 'products/category.html'
    context_object_name = 'categ'

class SubsCategoryView(ListView):
    model = SubsCategory 
    template_name = 'products/category.html'
    context_object_name = 'subc'



from .models import Product1
from django.utils import timezone

# SHOP
def shop(request):
    q= request.GET.get('q')
    products = Product1.objects.all()
    if q :
        instance = SubsCategory.objects.get(slug=q)
        products = products.filter(subscategory=instance)


    current_time = timezone.now()
    producttwo = Product1.objects.all()
    categories = Categorys.objects.all()  # Get all categories
    subcategory = SubsCategory.objects.all()

   
    
    context = {"is_shop": True,
               'products': products,
               'current_time': current_time,
               'producttwo': producttwo,
               'categories': categories,
               'subcategory':subcategory,
            
               }
    return render(request, "products/products.html", context)