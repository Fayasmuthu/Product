from django.contrib import admin
from .models import (
    Category, SubCategory, Product, Product1, Categorys, SubsCategory,
    Size, Filter_Price, Color, Brand, Product_tag
)
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
    list_display = ('title', 'slug','Category')  # Assuming you have a 'category' ForeignKey field in SubCategory model
    prepopulated_fields = {'slug': ('title',)}



class Product1Admin(admin.ModelAdmin):
    list_display = ('name', 'vendor', 'original_price', 'sale_price', 'sale_end_date')
    list_filter = ('vendor', 'sale_end_date')
    search_fields = ('name', 'vendor')
    list_editable = ('sale_price', 'sale_end_date')

admin.site.register(Product1, Product1Admin)
admin.site.register(Filter_Price)
admin.site.register(Color)

admin.site.register(Size)
admin.site.register(Brand)
admin.site.register(Product_tag)
