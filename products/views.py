from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView ,TemplateView 
from django.views.generic.edit import FormView
from .models import Product ,Categorys,SubsCategory
 
# Create your views here.

class Product(ListView):
    model = Product 
    template_name = 'products/test.html'
    context_object_name = 'products'

class CategorysView(ListView):
    model = Categorys 
    template_name = 'products/category.html'
    context_object_name = 'categ'

class SubsCategoryView(ListView):
    model = SubsCategory 
    template_name = 'products/category.html'
    context_object_name = 'subc'



from .models import Product1,Filter_Price,Color,Size,Brand,Product_tag
from django.utils import timezone

# SHOP
def shop(request):
    categories = Categorys.objects.all()  
    subcategory = SubsCategory.objects.all()
    filter_price =Filter_Price.objects.all()
    colors=Color.objects.all()
    sizes =Size.objects.all()
    brands =Brand.objects.all()
    product_tag=Product_tag.objects.all()
    

    q= request.GET.get('q')
    selected_price =request.GET.get('price')
    selected_color=request.GET.get('color')
    selected_size =request.GET.get('size')
    selected_brand =request.GET.getlist('brand')
    selected_tag =request.GET.get('tag')
    products = Product1.objects.all()
    
    if q :
        instance = SubsCategory.objects.get(slug=q)
        products = products.filter(subscategory=instance)

    if selected_color:
        products= products.filter(color__name=selected_color)

    if selected_size :
        products =products.filter(size__title=selected_size)
    
    if selected_price :
        products =products.filter(price__price=selected_price)
    
    if selected_brand :
        products =products.filter(brand__name__in=selected_brand)

    if selected_tag :
        products =products.filter(products_tag__name=selected_tag)

    


    current_time = timezone.now()
   
    context = {"is_shop": True,
               'products': products,
               'current_time': current_time,
               'categories': categories,
               'subcategory':subcategory,
               'filter_price':filter_price,
               'colors':colors,
               'sizes': sizes,
               'brands':brands,
               'product_tag':product_tag,
               'selected_size': selected_size, 
            
               }
    return render(request, "products/products.html", context)