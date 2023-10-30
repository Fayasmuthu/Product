from django.contrib import admin
from products.models import Product1, Categorys, SubsCategory,ProductFeature,ProductAdditional
from .models import (
    Category, SubCategory, Product, 
    Size, Color, Brand, Product_tag,ProductImage,
    AvilableSize
)
from django.utils.safestring import mark_safe


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'Category')  # Assuming you have a 'category' ForeignKey field in SubCategory model
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price' , 'SubCategory' )  # Assuming you have a 'subcategory' ForeignKey field in Product model
    prepopulated_fields = {'slug': ('title',)}


# ---------TWO-------
@admin.register(Categorys)
class CategorysAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(SubsCategory)
class SubsCategoryAdmin(admin.ModelAdmin):
    list_display = ("title",'Category' )
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("title",'Category' )
    # autocomplete_fields = ("Category",)
    search_fields = (
        "title",
        'Category__title',
    )

    

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0

class ProductFeatureInline(admin.TabularInline):
    model = ProductFeature
    extra = 0

class AvailableSizeInline(admin.TabularInline):
    model = AvilableSize
    extra = 0
    autocomplete_fields = ('size',)


class ProductAdditionalInline(admin.TabularInline):
    model = ProductAdditional
    extra = 0
    max_num =1

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Product_tag)
class Product_tagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug','background_color')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Product1)
class Product1Admin(admin.ModelAdmin):
    list_display = ("name",'p_subscategory','image_preview' )
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ('p_subscategory', 'name')
    autocomplete_fields = ("p_subscategory","brand")
    inlines = [ProductAdditionalInline,ProductFeatureInline,ProductImageInline,AvailableSizeInline]
    search_fields = (
        "name",
        'p_subscategory__name',
    )

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img loading="lazy" src="{obj.image.url}" style="width:50px;height:50px;object-fit:contain;">'
            )
        return None

    image_preview.short_description = 'Image Preview'



@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('title', 'code')
    search_fields = ('title',)


@admin.register(AvilableSize)
class AvilableSizeAdmin(admin.ModelAdmin):
    list_display = ('product', 'size')
    search_fields = ('product__name',)
    autocomplete_fields = ('product', 'size')


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name','code','color_bg')

    def color_bg(self,obj):
        return mark_safe('<div style="width:30px; height:30px; background-color:%s"></div>' % (obj.code))
       
    color_bg.short_description = 'color_bg'