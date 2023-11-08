from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView ,TemplateView ,DetailView
from django.views.generic.edit import FormView
from .models import Product ,Categorys,SubsCategory
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from .models import Product1,Color,Size,Brand,Product_tag,AvilableSize
from django.utils import timezone
from django.db.models import Min
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

 
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





# SHOP
def shop(request):
    categories = Categorys.objects.all()  
    subcategory = SubsCategory.objects.all()
    colors=Color.objects.all()
    sizes =Size.objects.all()
    brands =Brand.objects.all()
    product_tag=Product_tag.objects.all()
    

    q= request.GET.get('q')
    selected_price =request.GET.get('amount', '')
    print('selected_price=',selected_price)
    selected_color=request.GET.get('color')
    selected_size =request.GET.get('size')
    selected_brand =request.GET.getlist('brand')
    selected_tag =request.GET.get('tag')
    azid = request.GET.get('SortBy')
    category=request.GET.get('Category')
    
    products = Product1.objects.all()
    
    if q :
        instance = SubsCategory.objects.get(slug=q)
        products = products.filter(p_subscategory=instance)

    if category :
        products = products.filter(p_subscategory__Category__slug=category)

    if selected_color:
        products= products.filter(productimage__color__name=selected_color)

    if selected_size :
        products =products.filter(available_sizes__size__code=selected_size)
    
    if selected_price :
        # products =products.filter(price__price=selected_price)
        selected_price = selected_price.replace('$','')
        print('selected_pric222e=',selected_price)
        try:
            min_amount, max_amount = map(int,selected_price.split('-'))
            products=products.filter(available_sizes__price__gte=min_amount,
                                     available_sizes__price__lte=max_amount
                                     ).distinct()
            
        except ValueError:
            print("ValueError")
    if selected_brand :
        products =products.filter(brand__name__in=selected_brand)

    if selected_tag :
        products =products.filter(products_tag__name=selected_tag)
    


    if azid == 'name-ascending':
        products = products.order_by('name')

    if azid == 'name-descending':
        products = products.order_by('-name')
        


    current_time = timezone.now()
   
    context = {"is_shop": True,
               'products': products,
               'current_time': current_time,
               'selected_size': selected_size,
               'stars': range(1, 6),
               'product_tag':product_tag,
                'applied_filters': {
                    'categories': categories,
                    'subcategory':subcategory,
                    'colors':colors,
                    'sizes': sizes,
                    'brands':brands,
                    
                }
           
               }
    return render(request, "products/products.html", context)
#INDEX
def home(request):
    categories = Categorys.objects.all()
    subcategories = SubsCategory.objects.filter(is_popular=True)
    best_sellers=Product1.objects.filter(is_best_seller=True)[:8]
    new_arrivals=Product1.objects.filter(is_new_arrival=True)[:8]
    top_rated=Product1.objects.filter(is_top_rated=True)[:8]
    context ={
        'categories':categories,
        'subcategories':subcategories,
        'best_sellers':best_sellers,
        'new_arrivals':new_arrivals,
        'top_rated':top_rated,
        'stars': range(1, 6)
        
    }
    return render(request,"products/index.html",context)

#PRODUCT_DETAIL
class products_detailsViews(DetailView):
    model = Product1
    template_name = 'products/product-layout1.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        # product = context['product']  # Assuming the product object is available in the context
        # stars = range(1, product.rating + 1)  # Generating stars based on the product's rating
        stars = range(1, 6)  # Generating stars based on the product's rating

        context['stars'] = stars
       
        return context

#LOGIN   
def login(request):
    # if request.method=="POST":
    #     username=request.POST["customer[username]"]
    #     password=request.POST["customer[password]"]
    #     user = authenticate(request,username=username,password=password )
    #     if user is not None:
    #         login(request,user)
    #         messages.success(request,('You have been logged In...'))
    #     else:
    #         login(request,user)
    #         messages.success(request,('There was an Error, Please try again'))
    # else:
    return render(request,"account/login.html")   
#LOGOUT
def logout(request):
    # logout(request)
    # messages.success(request,("You have been logged out....."))
    return redirect("products:index")
#REGISTER
def register(request):
    return render(request,"account/register.html")

# @login_required(login_url="login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product1.objects.get(id=id)
    cart.add(product=product)
    return redirect("products:products")


# @login_required(login_url="login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product1.objects.get(id=id)
    cart.remove(product)
    return redirect("products:cart_detail")


# @login_required(login_url="login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product1.objects.get(id=id)
    cart.add(product=product)
    return redirect("products:cart_detail")


# @login_required(login_url="login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product1.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("products:cart_detail")


# @login_required(login_url="login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("products:cart_detail")


# @login_required(login_url="/users/login")
def cart_detail(request):
    return render(request, 'cart/cart-style.html')



