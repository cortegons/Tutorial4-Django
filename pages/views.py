from typing import Any
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView
from django.views import View
from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .utils import ImageLocalStorage
# Create your views here.

#def homePageView(request):
#    return HttpResponse('Hello World')

class homePageView(TemplateView):
    template_name = "home.html"


class AboutPageView(TemplateView):
    template_name = "about.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "About us - Online Store",
            "subtitle": "About us",
            "description": "This is an about page...",
            "author": "Developed by: Camilo Ortegon",
        })
        
        return context
    
class ContactPageView(TemplateView):
    template_name = "contact.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Contact us - Online Store",
            "subtitle": "Contact us",
            "email": "example@mail.com",
            "address": "17 St 8B-10",
            "phonenumber": "1234567890"
        })
        
        return context

"""
class Product:
    products = [
        {"id":"1", "name":"TV", "description":"Best TV", "price": 300},
        {"id":"2", "name":"iPhone", "description":"Best iPhone", "price": 500},
        {"id":"3", "name":"Chromecast", "description":"Best Chromecast", "price": 400},
        {"id":"4", "name":"Glasses", "description":"Best Glasses", "price": 60},
    ]
"""
class ProductIndexView(View):
    template_name = "products/index.html"
    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.objects.all()
        
        return render(request, self.template_name, viewData)
    
class ProductShowView(View):
    template_name = 'products/show.html'
    def get(self, request, id):
        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError("Product id must be 1 or greater")
            product = get_object_or_404(Product, pk=product_id)
        except (IndexError, ValueError):
            return HttpResponseRedirect(reverse("home"))

        viewData = {}
        product = get_object_or_404(Product, pk=product_id)
        viewData["title"] = product.name + ' - Online Store'
        viewData["subtitle"] = product.name + " - Product information"
        viewData["product"] = product
            
        return render(request, self.template_name, viewData)
        
        
    
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price']    
    def clean(self):
        price = self.cleaned_data.get("price")
        if price is not None and price <= 0:
            raise forms.ValidationError("Price can't be less or equal zero")
    
class ProductCreateView(View):
    template_name = "products/create.html"
    created_template_name = "products/created.html"
    
    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Create product"
        viewData["form"] = form
        
        return render(request, self.template_name, viewData)
    
    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, self.created_template_name, {"title": "Product created"})
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)
        
class CartView(View):
    template_name = "cart/index.html"
    
    def get(self, request):
        products = {}
        products[12] = {"name": "Tv Samsung", "price": "1000"}
        products[11] = {"name": "Iphone", "price": "2000"}
        
        cart_products = {}
        cart_product_data = request.session.get("cart_product_data", {})
        
        for key, product in products.items():
            if str(key) in cart_product_data.keys():
                cart_products[key] = product
                
        view_data = {
            "title": "Cart - Online Store",
            "subtitle": "Shopping Cart",
            "products": products,
            "cart_products": cart_products
        }
        
        return render(request, self.template_name, view_data)
    
    def post(self, request, product_id):
        cart_product_data = request.session.get("cart_product_data", {})
        cart_product_data[product_id] = product_id
        request.session["cart_product_data"] = cart_product_data
        
        return redirect("cart_index")
    
class CartRemoveAllView(View):
    def post(self, request):
        if "cart_product_data" in request.session:
            del request.session["cart_product_data"]
            
        return redirect("cart_index")
    
def ImageViewFactory(image_storage):
    class ImageView(View):
        template_name = 'images/index.html'

        def get(self, request):
            image_url = request.session.get('image_url', '')
            return render(request, self.template_name, {'image_url': image_url})

        def post(self, request):
            image_url = image_storage.store(request)
            request.session['image_url'] = image_url
            return redirect('image_index')

    return ImageView

class ImageViewNoDI(View): 
    template_name = 'images/index.html'

    def get(self, request):
        image_url = request.session.get('image_url', '')
        return render(request, self.template_name, {'image_url': image_url}) 
    
    def post(self, request):
        image_storage = ImageLocalStorage()
        image_url = image_storage.store(request) 
        request.session['image_url'] = image_url

        return redirect('image_index')
