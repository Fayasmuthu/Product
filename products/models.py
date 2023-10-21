from django.db import models
from tinymce.models import HTMLField


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
    image =models.ImageField(upload_to='category')
    
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
    vendor = models.CharField(max_length=255)
    image = models.ImageField(upload_to='subcategory')

    class Meta:
        ordering = ('id',)
        verbose_name = ('SubCategory')
        verbose_name_plural = ('SubCategories')

    def __str__(self):
        return str(self.title)


class Product1(models.Model):
    subscategory =models.ForeignKey(SubsCategory,on_delete=models.CASCADE,related_name='subscategory')
    name = models.CharField(max_length=255)
    description = models.TextField()
    vendor = models.CharField(max_length=255)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    image2 = models.ImageField(upload_to='products/')
    sale_end_date = models.DateField()
    # You might have additional fields like reviews and colors.

    def is_on_sale(self):
        from django.utils import timezone
        return self.sale_end_date > timezone.now()
    
    class Meta:
        ordering = ('id',)
        verbose_name = ('products ')
        verbose_name_plural = ('Product')

    def __str__(self):
        return self.name