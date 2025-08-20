from django.shortcuts import render
from django.views.generic import (
    ListView, DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import (
    Product, Size, Manufacturer, Category,
)

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'stores/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        queryset = Product.objects.all()
        q_name = self.request.GET.get('product_name')
        q_type = self.request.GET.get('product_type_name')
        q_manufacturer = self.request.GET.get('manufacturer_name')
        q_category = self.request.GET.get('category_name')
        q_size = self.request.GET.get('sizes')

        if q_name:
            queryset = queryset.filter(name__icontains=q_name)
        if q_type:
            queryset = queryset.filter(product_type__name__icontains=q_type)
        if q_manufacturer:
            queryset = queryset.filter(manufacturer__name__icontains=q_manufacturer)
        if q_category:
            queryset = queryset.filter(category__name__icontains=q_category)
        if q_size:
            queryset = queryset.filter(sizes__full_name=q_size)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_name'] = self.request.GET.get('product_name', '')
        context['product_type_name'] = self.request.GET.get('product_type_name', '')
        context['manufacturer_name'] = self.request.GET.get('manufacturer_name', '')
        context['category_name'] = self.request.GET.get('category_name', '')
        context['sizes'] = self.request.GET.get('sizes', '')

        context['all_manufacturers'] = Manufacturer.objects.all()
        context['all_categories'] = Category.objects.all()
        context['all_sizes'] = Size.objects.all()
        return context
    
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'stores/product_detail.html'
    
   

