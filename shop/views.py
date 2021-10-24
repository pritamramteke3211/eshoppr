
from django.shortcuts import render,redirect,HttpResponseRedirect,HttpResponse
from django.views import View
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import *
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.core.paginator import  Paginator


class ShopHomePage(View):
    template_name = 'shop/home.html'
    def get(self, request):
        products = Product.objects.all()
        clothes = Product.objects.filter(category='Clothes')
        electronics = Product.objects.filter(category='Electronics')
        context = {'products':products,'clothes':clothes, 'electronics':electronics, 'home':'active'}
        return render(request,self.template_name,context)


@method_decorator(login_required, name='dispatch')
class UserProfile(View):
    template_name = 'shop/dashboard.html'
    def get(self, request):
        context = {'dashboard':'active'}
        return render(request,self.template_name,context)

def search(request):
    equery = request.GET.get('search')
    query = equery
    if query:
        query = query.strip()
        query = query.lower()
        prods = Product.objects.values('product_name','category','sub_category')
        prods_name_list  = [i['product_name'] for i in prods]
        prods_category_list  = [i['category'] for i in prods]
        prods_brand_list  = [i['sub_category'] for i in prods]

        prod_product_id = []
        for i in prods_name_list:
            if i.lower() == query:
                item = Product.objects.get(product_name = i)
                if item:
                    prod_product_id.append(item.product_id)
            else:
                for  j in i.split():
                    if j.lower() == query:
                        item = Product.objects.get(product_name = i)
                        if item:
                            prod_product_id.append(item.product_id)

        for i in prods_category_list:
                if i.lower() == query:
                    item = Product.objects.filter(category = i)
                    if item:
                        for i in item:
                            prod_product_id.append(i.product_id)

        for i in prods_brand_list:
                if i.lower() == query:
                    item = Product.objects.filter(sub_category = i)
                    if item:
                        for i in item:
                            prod_product_id.append(i.product_id)

        prod_product_id = set(prod_product_id)
        prod_product_id = list(prod_product_id)
        products = Product.objects.filter(pk__in=prod_product_id).order_by('product_id')

        paginator = Paginator(products, 3, orphans=1)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    else:
        products = Product.objects.none()
        page_obj = None

    context = {'products':products, 'query':equery,'page_obj':page_obj}
    return render(request,'shop/search.html', context)






@login_required(redirect_field_name='login',login_url='/login')
def add_to_cart(request,product_id=None):
    product = Product.objects.get(product_id=product_id)
    if request.user.is_authenticated:
        user = request.user
        cart = Cart(user=user, product_name=product)
        cart.save()
    else:
        messages.warning(request,'Login First')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) ## return to same page 

@login_required(redirect_field_name='login',login_url='/login')
def buy_now(request,product_id):
    product = Product.objects.get(product_id=product_id)
    if request.user.is_authenticated:
        user = request.user
        cart = Cart(user=user, product_name=product)
        cart.save()
        return redirect('checkout')
    else:
        messages.warning(request,'Login First')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 

@login_required(redirect_field_name='login',login_url='/login')
def mycart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        tot_price = 0
        for product in cart:
            tot_price += product.product_name.price * product.quantity
        context = {'cart':cart,'tot_price':tot_price,'mycart':'active'}
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 

    return render(request,'shop/mycart.html', context)

def quantity_plus(request,cart_id):
    cart_prod = Cart.objects.get(id=cart_id)
    cart_prod.quantity += 1
    cart_prod.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) ## return to same page 
    # return redirect('mycart')

def quantity_minus(request,cart_id):
    cart_prod = Cart.objects.get(id=cart_id)
    if cart_prod.quantity > 1:
        cart_prod.quantity -= 1
        cart_prod.save()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) ## return to same page 
    return redirect('mycart')

def remove_cart(request,cart_id):
    cart_prod = Cart.objects.get(id=cart_id)
    cart_prod.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) ## return to same page
    # return redirect('mycart')

def clear_cart(request):
    cart = Cart.objects.filter(user=request.user)
    cart.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) ## return to same page

@method_decorator(login_required, name='dispatch')
class Checkout(View):
    template_name = 'shop/checkout.html'
    def get(self, request):
        if request.method == 'POST':
            form = AddressForm(request.POST)
            if form.is_valproduct_id():
                form.save()
        else:
            form = AddressForm()
        cart = Cart.objects.filter(user=request.user)
        addresses = Address.objects.filter(Q(user=request.user) & Q(delivery_address=True))
        tot_price = 0
        for product in cart:
            tot_price += product.product_name.price * product.quantity
        context={'cart':cart,'addresses':addresses, 'tot_price':tot_price, 'form':form}
        return render(request,self.template_name,context)
    
@login_required(redirect_field_name='login',login_url='/login')
def productview(request,product_id=None):
    product = Product.objects.get(product_id=product_id)
    context ={'product':product}
    return render(request,'shop/productview.html',context)

@login_required(redirect_field_name='login',login_url='/login')
def address(request):
    addresses = Address.objects.filter(user=request.user)
    context = {'addresses':addresses}
    return render(request,'shop/address.html',context)

@login_required(redirect_field_name='login',login_url='/login')
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            phone = form.cleaned_data['phone_number']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zip = form.cleaned_data['zip']
            
         
            user = User.objects.get(username=request.user)
            addresses = Address.objects.filter(user=request.user)
            if len(addresses) == 0:
                delivery_address = True
            else:
                delivery_address = False

            name = user.first_name + ' ' + user.last_name
             


            fm = Address(user=request.user, name=name, email=user.email, phone_number=phone, address=address, city=city, state=state, zip= zip,delivery_address=delivery_address)
            fm.save()
            messages.success(request,'Your Address Added Successfully')
            return redirect('address')
    else:
        form = AddressForm()
    context = {'form':form}
    return render(request,'shop/add_address.html',context)

def delete_address(request,product_id=None):
    address = Address.objects.get(pk=product_id)
    address.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) ## return to same page

@login_required(redirect_field_name='login',login_url='/login')
def order_placed(request):
    return render(request,'shop/odered_placed.html')


def order(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        address = Address.objects.filter(Q(user=request.user) & Q(delivery_address=True))[0]
        
        product_count = len(cart)
        temp = 0
        for i in cart:
            temp += i.product_name.price * i.quantity
        total_price = temp + 70
        order = Order(user=request.user,product_count=product_count,total_amount=total_price,order_date=timezone.now())
        order.save()
        
        if address:
            ord_address = Ordered_Address(user=request.user,order=order,address=address.address,phone_number=address.phone_number,city=address.city,state=address.state,zip=address.zip)
            ord_address.save()
        else:
            messages.warning(request, 'Default Delivery Adrress not set')

        for i in cart:
            product = i.product_name
            quantity = i.quantity
            ord_prod = Ordered_Product(order=order,product=product,quantity=quantity)
            ord_prod.save()

        
        cart.delete()
    
        return redirect('order_placed')
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) ## return to same page


@csrf_exempt
def handlerequest(request):
    return HttpResponse('done')

@login_required(redirect_field_name='login',login_url='/login')
def orders(request):
    orders  = Order.objects.filter(user=request.user)
    context = {'orders':orders}
    return render(request,'shop/orders.html',context)

def cancel_order(request,id=None):
    order = Order.objects.get(pk=id)
    print(order.status)
    if order.status == 'On The Way' or order.status == 'Delivered':
        messages.warning(request,f'Soory, You Can\'t Cancel This Order Now')
    else:
        messages.success(request,f'Order Cancelled Successfully')
        order.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) ## return to same page

@login_required(redirect_field_name='login',login_url='/login')
def change_shipping_adrress(request):
    if request.method == 'POST':
        id = request.POST.getlist('address')
        id = int(*id)
        print(id)

        address = Address.objects.get(pk=id)
        address.delivery_address = True
        address.save()
        print(address)

        addresses = Address.objects.filter(user=request.user).exclude(pk=id)
        print(addresses)
        
        for i in addresses:
            i.delivery_address = False
            i.save()

        messages.success(request,'Adress Changed')
        return redirect('checkout')

    adrresses = Address.objects.filter(user=request.user)
    context = {'adrresses':adrresses}
    return render(request, 'shop/change_shipping_address.html',context)

