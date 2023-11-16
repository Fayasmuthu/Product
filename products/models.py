from django.db import models
from tinymce.models import HTMLField
from django import template
from colorfield.fields import ColorField
from django.core.validators import MaxValueValidator
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User


register = template.Library()
# Create your models here.
class Category(models.Model):
    title =models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    class Meta:
        ordering = ('id',)
        verbose_name = ('Category')
        verbose_name_plural = ('TestCategories')

    def __str__(self):
        return str(self.title)
    
class SubCategory(models.Model):
    Category= models.ForeignKey(Category,on_delete=models.CASCADE,related_name='category')
    title =models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)


    class Meta:
        ordering = ('id',)
        verbose_name = ('SubCategory')
        verbose_name_plural = ('TestSubCategories')

    def __str__(self):
        return str(self.title)
    
class Product(models.Model):
    SubCategory = models.ForeignKey(SubCategory,on_delete=models.CASCADE,related_name='SubCategory')
    title =models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    price =models.DecimalField(max_digits=10,decimal_places=2)
    description =HTMLField()
    image =models.ImageField(upload_to='Whoesale/products')

    class Meta:
        ordering = ('id',)
        verbose_name = ('products ')
        verbose_name_plural = ('Testproductold')

    def __str__(self):
        return str(self.title)
    
class cor(models.Model):
    name=models.CharField(max_length=12)

# -----------second---------

class Categorys(models.Model):
    title =models.CharField(max_length=100)
    slug = models.SlugField(max_length=100,unique=True)
    image =models.ImageField(upload_to="category/",blank=True,null=True)  
    
    
    class Meta:
        ordering = ('id',)
        verbose_name = ('Category')
        verbose_name_plural = ('Category')

    def get_subcategories(self):
        return SubsCategory.objects.filter(category=self)
    def __str__(self):
        return str(self.title)


class SubsCategory(models.Model):
    Category= models.ForeignKey(Categorys,on_delete=models.CASCADE,related_name='category')
    title =models.CharField(max_length=100)
    slug = models.SlugField(max_length=100,unique=True)
    image =models.ImageField(upload_to="sub/")
    is_popular = models.BooleanField(default=True)

    class Meta:
        ordering = ('id',)
        verbose_name = ('SubCategory')
        verbose_name_plural = ('SubCategories')

    def __str__(self):
        return str(self.title)
    
    def get_product_count(self):
        return Product1.objects.filter(p_subscategory=self).count()


    
class Color(models.Model):
    name=models.CharField(max_length=200)
    code =ColorField(default='#FF0000')

    def __str__(self):
        return self.name
    



class Size(models.Model):
    title =models.CharField(max_length=50)
    code = models.CharField(max_length=255,unique=True)
    available =models.BooleanField(default=True)

    def __str__(self):
        return str(self.title)


class Brand(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product_tag(models.Model):
    name =models.CharField(max_length=100,unique=True)
    slug =models.SlugField(unique=True)
    background_color=models.ForeignKey('products.Color',on_delete=models.CASCADE,blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Product1(models.Model):
    CONDITION=(('New','New'),('Old','Old'))
    STOCK=(('IN STOCK','IN STOCK'),('OUT OF STOCK','OUT OF STOCK'))
    STATUS=(('Publish','Publish'),('Draft','Draft'))

    p_subscategory =models.ForeignKey(SubsCategory,on_delete=models.CASCADE,related_name='subscategory')
    name = models.CharField(max_length=255)
    slug=models.SlugField(max_length=100)
    description = models.TextField()
    vendor = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/')
    # sale_end_date = models.DateField(blank=True,null=True)
    available = models.BooleanField(default=True) 
    brand =models.ForeignKey(Brand,on_delete=models.CASCADE,related_name='brand')
    products_tag=models.ForeignKey(Product_tag,on_delete=models.CASCADE,related_name='p_tag',blank=True,null=True)
    rating =models.PositiveIntegerField(
        validators=[MaxValueValidator(5)],default=5,verbose_name="Product Rating(max:5)"
    )
    condition=models.CharField(choices=CONDITION,max_length=200)
    stock=models.CharField(choices=STOCK,max_length=200)
    status=models.CharField(choices=STATUS,max_length=200)
    is_best_seller = models.BooleanField(default=True)
    is_new_arrival = models.BooleanField(default=True)
    is_top_rated = models.BooleanField(default=True)
    # You might have additional fields like reviews and colors.

    def is_on_sale(self):
        from django.utils import timezone
        return self.sale_end_date > timezone.now()
    
    class Meta:
        ordering = ('id',)
        verbose_name = ('products ')
        verbose_name_plural = ('Product')

    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        super(Product1, self).delete(*args, **kwargs)
        storage.delete(path)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
  
    
    def get_images(self):
        return ProductImage.objects.filter(product=self)

    def get_additional(self):
        return ProductAdditional.objects.filter(product=self).first()
    
    def get_features(self):
        return ProductFeature.objects.filter(product=self)

    def get_colors(self):
         return ProductImage.objects.filter(product=self).distinct()

    def get_sizes(self):
        return AvilableSize.objects.filter(product=self)

    def get_sale_price(self):
        return min([p.price for p in self.get_sizes()])

    def get_original_price(self):
        sizes = self.get_sizes()
        valid_prices = [p.original_price for p in sizes if p.original_price is not None]
        return min(valid_prices) if valid_prices else None

    def get_offer_percent(self):
        return min([p.offer_percent() for p in self.get_sizes()])

    def get_absolute_url(self):
        return reverse("products:products_details", kwargs={"slug": self.slug})

    def related_products(self):
        return Product1.objects.filter().exclude(pk=self.pk).distinct()[0:12]
    
    def get_Countdown(self):
        return Countdown.objects.filter(product=self)
    

    def get_availsold(self):
        return Availability_sold.objects.filter(product=self)

    def __str__(self):
        return f"{self.brand}: {self.name}"
    
    def get_review(self):
        return Review.objects.filter(product=self)


class ProductImage(models.Model):
    product = models.ForeignKey(Product1, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products',blank=True,null=True)
    color = models.ForeignKey('products.Color', on_delete=models.CASCADE,blank=True,null=True)

    class Meta:
        verbose_name = ("Product Image")
        verbose_name_plural = ("Product Images")
        ordering = ("product",)

    def __str__(self):
        return str(self.name)
    

class ProductFeature(models.Model):
    product = models.ForeignKey(Product1, on_delete=models.CASCADE)
    point = models.TextField(max_length=500)

    class Meta:
        verbose_name = ("Product Feature")
        verbose_name_plural = ("Product Features")
        ordering = ("point",)

    def __str__(self):
        return f"{self.point}"


class ProductAdditional(models.Model):
    product = models.ForeignKey(Product1, on_delete=models.CASCADE)
    manufacturer = models.CharField(max_length=150,blank=True,null=True)
    dimension = models.CharField(max_length=150,blank=True,null=True)
    first_available =models.DateField(blank=True,null=True)
    
    class Meta:
        verbose_name = ("Product Additional")
        verbose_name_plural = ("Product Additionals")
        ordering = ("id",)

    def __str__(self):
        return f"{self.manufacturer}"


class AvilableSize(models.Model):
    product=models.ForeignKey(Product1,on_delete=models.CASCADE, related_name='available_sizes')
    size =models.ForeignKey('products.Size',on_delete=models.CASCADE,blank=True,null=True)
    color = models.ForeignKey('products.Color', on_delete=models.CASCADE,blank=True,null=True)
    price =models.DecimalField(max_digits=10, decimal_places=2) 
    original_price=models.FloatField(blank=True, null=True)
    opening_stock=models.IntegerField()
    minimum_order_qty=models.IntegerField()

    class Meta:
        ordering = ("price",)
        verbose_name = ("Available Size")
        verbose_name_plural = ("Available Sizes")

    def __str__(self):
        return f"{self.color} / {self.size} - {self.price}"

    def save(self, *args, **kwargs):
        if self.original_price is None:
            self.original_price = self.price
        super().save(*args, **kwargs)


class Countdown(models.Model):
    product=models.ForeignKey(Product1,on_delete=models.CASCADE)
    sale_end_date = models.DateField(blank=True,null=True)

    class Meta:
        ordering = ("id",)
        verbose_name = ("Offer Count")
        verbose_name_plural = ("Offer Count")

class Availability_sold(models.Model):
    product=models.ForeignKey(Product1,on_delete=models.CASCADE)
    availability_sold = models.PositiveIntegerField(blank=True,null=True)
    availability_available = models.PositiveIntegerField(blank=True,null=True)
    availability_progress = models.PositiveIntegerField(blank=True,null=True)

    class Meta:
        ordering = ("id",)
        verbose_name = ("Offer Count")
        verbose_name_plural = ("Offer Count")


class Review(models.Model):
    product=models.ForeignKey(Product1,on_delete=models.CASCADE)
    name=models.CharField(max_length=150)
    email=models.EmailField()
    review_title=models.CharField(max_length=150)
    rating =models.IntegerField()
    review_text=models.TextField(max_length=200)
    create_at =models.DateTimeField(auto_now_add=True)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product1, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

