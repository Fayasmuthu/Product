from django.db import models
from tinymce.models import HTMLField
from django import template
from colorfield.fields import ColorField
from django.core.validators import MaxValueValidator
from django.template.defaultfilters import slugify
from django.urls import reverse

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
    
    
    class Meta:
        ordering = ('id',)
        verbose_name = ('Category')
        verbose_name_plural = ('Category')

    def __str__(self):
        return str(self.title)


class SubsCategory(models.Model):
    Category= models.ForeignKey(Categorys,on_delete=models.CASCADE,related_name='category')
    title =models.CharField(max_length=100)
    slug = models.SlugField(max_length=100,unique=True)
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
    slug =models.SlugField()
    background_color=models.ForeignKey('products.Color',on_delete=models.CASCADE,blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Product1(models.Model):
    p_subscategory =models.ForeignKey(SubsCategory,on_delete=models.CASCADE,related_name='subscategory')
    name = models.CharField(max_length=255)
    slug=models.SlugField(max_length=100)
    description = models.TextField()
    vendor = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/')
    sale_end_date = models.DateField()
    available = models.BooleanField(default=True) 
    brand =models.ForeignKey(Brand,on_delete=models.CASCADE,related_name='brand')
    products_tag=models.ForeignKey(Product_tag,on_delete=models.CASCADE,related_name='p_tag')
    rating =models.PositiveIntegerField(
        validators=[MaxValueValidator(5)],default=5,verbose_name="Product Rating(max:5)"
    )
    is_new_arrival = models.BooleanField(default=True)
    is_best_seller = models.BooleanField(default=True)
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
        return ProductAdditional.objects.filter(product=self)
    
    def get_features(self):
        return ProductFeature.objects.filter(product=self)

    def get_colors(self):
         return ProductImage.objects.filter(product=self).distinct()

    def get_sizes(self):
        return AvilableSize.objects.filter(product=self)

    def get_sale_price(self):
        return min([p.sale_price for p in self.get_sizes()])

    def get_original_price(self):
        sizes = self.get_sizes()
        valid_prices = [p.original_price for p in sizes if p.original_price is not None]
        return min(valid_prices) if valid_prices else None

    def get_offer_percent(self):
        return min([p.offer_percent() for p in self.get_sizes()])

    def get_absolute_url(self):
        return reverse("products:product_detail", kwargs={"pk": self.pk})

    def related_products(self):
        return Product1.objects.filter(subcategory__in=self.p_subscategory.all()).exclude(pk=self.pk).distinct()[0:12]

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product1, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products')
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
    product=models.ForeignKey(Product1,on_delete=models.CASCADE)
    size =models.ForeignKey('products.Size',on_delete=models.CASCADE)
    sale_price =models.FloatField()
    original_price=models.FloatField(blank=True, null=True)
    opening_stock=models.IntegerField()
    minimum_order_qty=models.IntegerField()

    class Meta:
        ordering = ("sale_price",)
        verbose_name = ("Available Size")
        verbose_name_plural = ("Available Sizes")
