
from django.shortcuts import render,redirect
from django.views import View
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required

class ShopHomePage(View):
    template_name = 'shop/shome.html'
    def get(self, request):
        return render(request,self.template_name)

@login_required(redirect_field_name='login',login_url='/login/')
def add_to_cart(request,product_id=None):
    product = Product.objects.get(product_id=product_id)
    product_nm = product.product_name
    print(product_nm)
    user = request.user
    dup = False
    pcart =  Cart.objects.filter(user = request.user)
 
    for i in pcart:
        # print(i.product_name)
        if str(i.product_name) == str(product_nm):
            dup = True
   
    if dup:
        messages.warning(request,'You already Add this item')
    else:
        cart = Cart(user=user, product_name=product)
        cart.save()
    return redirect('home')

@login_required(redirect_field_name='login',login_url='/login/')
def mycart(request):
    cart = Cart.objects.filter(user=request.user)
    context = {'cart':cart}
    return render(request,'shop/mycart.html', context)

def about(request):
    return render(request,'shop/about.html')

def contact(request):
    return render(request,'shop/contact.html')

def tracker(request):
    return render(request,'shop/tracker.html')

def search(request):
    return render(request,'shop/search.html')

def productview(request):
    return render(request,'shop/productview.html')

def checkout(request):
    return render(request,'shop/checkout.html')