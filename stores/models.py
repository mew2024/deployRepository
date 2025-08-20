from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ProductType(models.Model):
    name = models.CharField(max_length=1000)
    
    class Meta:
        db_table = 'product_type'
        
    def __str__(self):
        return self.name
    
class Manufacturer(models.Model):
    name = models.CharField(max_length=1000)
    
    class Meta:
        db_table = 'manufacturer'
        
    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'category'
        
    def __str__(self):
        return self.name


class Size(models.Model):
    width = models.PositiveIntegerField()  # 例: 155
    aspect_ratio = models.PositiveIntegerField()  # 例: 65
    rim_diameter = models.PositiveIntegerField()  # 例: 14
    tire_type = models.CharField(max_length=1, choices=[('R', 'Radial'), ('B', 'Bias')], default='R')
    load_index = models.CharField(max_length=5, blank=True, null=True)  # 例: 75
    speed_symbol = models.CharField(max_length=1, blank=True, null=True)  # 例: L
    full_name = models.CharField(max_length=20, unique=True, blank=True)  # 追加

    class Meta:
        db_table = 'size'
        
    def save(self, *args, **kwargs):
        # full_name に __str__ と同じ値を入れる
        parts = f"{self.width}/{self.aspect_ratio}{self.tire_type}{self.rim_diameter}"
        if self.load_index:
            parts += self.load_index
        if self.speed_symbol:
            parts += self.speed_symbol
        self.full_name = parts
        super().save(*args, **kwargs)

    def __str__(self):
        parts = f"{self.width}/{self.aspect_ratio}{self.tire_type}{self.rim_diameter}"
        if self.load_index:
            parts += self.load_index
        if self.speed_symbol:
            parts += self.speed_symbol
        return parts


class Product(models.Model):
    name = models.CharField(max_length=1000)
    stock = models.PositiveIntegerField()
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    sizes = models.ManyToManyField(
        Size,
        related_name="products",
        blank=True,
        )  # 複数サイズを選択可能
    description = models.TextField(blank=True, null=True)
    price = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'product'
        
    def __str__(self):
        return self.name
    
class ProductPicture(models.Model):
    picture = models.FileField(upload_to='product_pictures/')
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='pictures',
    )
    order = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'product_picture'
        ordering = ['order']
        
    def __str__(self):
        return f'{self.product.name} - Picture {self.order}'

