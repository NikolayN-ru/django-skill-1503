from django.shortcuts import render
from .models import Product
from django.views.generic import ListView, DetailView

class ProductList(ListView):
	model = Product
	template_name = 'products.html'
	context_object_name = 'products'

class ProductDetail(DetailView):
	model = Product
	template_name = 'product.html'
	context_object_name = 'product'