from django.contrib import admin
from .models import ProductType, Manufacturer, Category, Size, Product, ProductPicture

# ProductPictureをProductにインライン表示する
class ProductPictureInline(admin.TabularInline):
    model = ProductPicture
    extra = 1  # 新規追加フォームを1つ表示
    ordering = ['order']  # 表示順序
    fields = ('picture', 'order')  # 編集可能なフィールド

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'product_type', 'manufacturer', 'category', 'price')
    filter_horizontal = ('sizes',)
    inlines = [ProductPictureInline]  # インライン追加

# 他のモデルも登録済みならそのまま
@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('id', 'width', 'aspect_ratio', 'rim_diameter', 'tire_type', 'load_index', 'speed_symbol')
    list_filter = ('tire_type',)