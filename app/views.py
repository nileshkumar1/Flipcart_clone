from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required 
from django.utils.decorators import method_decorator


# PRODUCT VIEW
class ProductView(View):
    def get(self, request):
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        mentopwears = Product.objects.filter(category='MT')
        menbottomwears = Product.objects.filter(category='MB')
        womentopwears = Product.objects.filter(category='WT')
        womenbottomwears = Product.objects.filter(category='WB')
        boyswears = Product.objects.filter(category='B')
        girlswears = Product.objects.filter(category='G')
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        
        return render(request, 'app/home.html', {'mentopwears':mentopwears,'menbottomwears':menbottomwears, 'womentopwears':womentopwears, 'womenbottomwears':womenbottomwears, 'boyswears':boyswears, 'girlswears':girlswears, 'topwears':topwears, 'bottomwears':bottomwears, 'mobiles':mobiles, 'laptops':laptops})


# PRODUCT DETAILS VIEW
class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
         item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart})


#ADD TO CART VIEW
@login_required
def add_to_cart(request):
   user = request.user
   product_id = request.GET.get('prod_id')
   product= Product.objects.get(id=product_id)
   Cart(user=user, product=product).save()
   return redirect('/cart')


#SHOW CART VIEW
@login_required
def show_cart(request):
   if request.user.is_authenticated:
      user = request.user
      cart = Cart.objects.filter(user=user)
      amount = 0.0
      shipping_amount = 50.0
      total_amount = 0.0
      cart_product = [p for p in Cart.objects.all() if p.user == user]

      if cart_product:
         for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount += temp_amount
            total_amount = amount + shipping_amount
         return render(request, 'app/addtocart.html', {'carts':cart, 'amount':amount, 'total_amount':total_amount})
      else:
         return render(request, 'app/emptycart.html')


#PLUS BUTTON VIEW
@login_required
def plus_cart(request):
   if request.method == 'GET':
      prod_id = request.GET['prod_id']
      print(prod_id)
      c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      c.quantity+=1
      c.save()
      amount = 0.0
      shipping_amount = 50.0
      cart_product = [p for p in Cart.objects.all() if p.user == request.user]
      
      for p in cart_product:
         temp_amount = (p.quantity * p.product.discounted_price)
         amount += temp_amount

      data={
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': amount + shipping_amount
         }
      return JsonResponse(data)


#MINUS BUTTON VIEW
@login_required
def minus_cart(request):
   if request.method == 'GET':
      prod_id = request.GET['prod_id']
      print(prod_id)
      c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      c.quantity-=1
      c.save()
      amount = 0.0
      shipping_amount = 50.0
      cart_product = [p for p in Cart.objects.all() if p.user == request.user]
      
      for p in cart_product:
         temp_amount = (p.quantity * p.product.discounted_price)
         amount += temp_amount
         

      data={
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': amount + shipping_amount
         }
      return JsonResponse(data)


# REMOVE CART BUTTON VIEW
@login_required
def remove_cart(request):
   if request.method == 'GET':
      prod_id = request.GET['prod_id']
      c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      c.delete()      
      amount = 0.0
      shipping_amount = 50.0
      cart_product = [p for p in Cart.objects.all() if p.user == request.user]
      
      for p in cart_product:
         temp_amount = (p.quantity * p.product.discounted_price)
         amount += temp_amount
         total_amount = amount

      data={
            'amount':amount,
            'total_amount': amount + shipping_amount
         }
      return JsonResponse(data)


# LOGIN VIEW
@login_required
def buy_now(request):
 return render(request, 'app/buynow.html')


# ORDER VIEW
@login_required
def orders(request):
   op = OrderPlaced.objects.filter(user=request.user)
   return render(request,'app/orders.html', {'order_placed':op})


# MOBILE VIEW
def mobile(request, data=None):
 if data == None:
    mobiles = Product.objects.filter(category='M')

 elif data == 'Redmi' or data == 'Oneplus' or data == 'Sony' or data == 'Realme' or data == 'Asus'or data == 'Samsung':
    mobiles = Product.objects.filter(category='M').filter(brand=data)
 
 elif data == 'Samsung':
    mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)

 elif data == 'Below':
    mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
 
 elif data == 'Above':
    mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)

 return render(request, 'app/mobile.html', {'mobiles':mobiles})


# LAPTOP VIEW
def laptop(request, data=None):
 if data == None:
    laptops = Product.objects.filter(category='L')

 elif data == 'Redmi' or data == 'MacBook' or data == 'hp' or data == 'dell' or data == 'Lenovo':
    laptops = Product.objects.filter(category='L').filter(brand=data)
 
 elif data == 'Below':
    laptops = Product.objects.filter(category='L').filter(discounted_price__lt=10000)
 
 elif data == 'Above':
    laptops = Product.objects.filter(category='L').filter(discounted_price__gt=10000)

 return render(request, 'app/laptop.html', {'laptops':laptops})


# TOPEWEAR VIEW
# def topwear(request, data=None):
#  if data == None:
#     topwears = Product.objects.filter(category='TW')

#  elif data == 'Denim' or data == 'Mufti' or data == 'BeingHuman' or data == 'JackJohn':
#     topwears = Product.objects.filter(category='TW').filter(brand=data)
 
#  elif data == 'Below':
#     topwears = Product.objects.filter(category='TW').filter(discounted_price__lt=10000)
 
#  elif data == 'Above':
#     topwears = Product.objects.filter(category='TW').filter(discounted_price__gt=10000)

#  return render(request, 'app/topwear.html', {'topwears':topwears})


# BOTTOMEWEAR VIEW
# def bottomwear(request, data=None):
#  if data == None:
#     bottomwears = Product.objects.filter(category='BW')

#  elif data == 'Denim' or data == 'Mufti' or data == 'BeingHuman' or data == 'JackJohn':
#     bottomwears = Product.objects.filter(category='BW').filter(brand=data)
 
#  elif data == 'Below':
#     bottomwears = Product.objects.filter(category='BW').filter(discounted_price__lt=10000)
 
#  elif data == 'Above':
#     bottomwears = Product.objects.filter(category='BW').filter(discounted_price__gt=10000)

#  return render(request, 'app/bottomwear.html', {'bottomwears':bottomwears})

#mentopwear
def mentopwear(request, data=None):
   if data == None:
      mentopwears = Product.objects.filter(category='MT')
   elif data == 'Denim' or data == 'Mufti' or data == 'BeingHuman' or data == 'JackJohn':
      mentopwears = Product.objects.filter(category='MT').filter(brand=data)
   elif data == 'Below':
      mentopwears = Product.objects.filter(category='MT').filter(discounted_price__lt=10000)
   elif data == 'Above':
      mentopwears = Product.objects.filter(category='MT').filter(discounted_price__gt=30000)
   return render(request, 'app/mentopwear.html', {'mentopwears':mentopwears})


#menbottomwear
def menbottomwear(request, data=None):
   if data == None:
      menbottomwears = Product.objects.filter(category='MB')
   elif data == 'Denim' or data == 'Mufti' or data == 'BeingHuman' or data == 'JackJohn':
      menbottomwears = Product.objects.filter(category='MB').filter(brand=data)
   elif data == 'Below':
      menbottomwears = Product.objects.filter(category='MB').filter(discounted_price__lt=10000)
   elif data == 'Above':
      menbottomwears = Product.objects.filter(category='MB').filter(discounted_price__gt=30000)
   return render(request, 'app/menbottomwear.html', {'menbottomwears':menbottomwears})

# womantop
def womentopwear(request, data=None):
   if data == None:
      womentopwears = Product.objects.filter(category='WT')
   elif data == 'Denim' or data == 'Mufti' or data == 'BeingHuman' or data == 'JackJohn':
      womentopwears = Product.objects.filter(category='WT').filter(brand=data)
   elif data == 'Below':
      womentopwears = Product.objects.filter(category='WT').filter(discounted_price__lt=10000)
   elif data == 'Above':
      womentopwears = Product.objects.filter(category='WT').filter(discounted_price__gt=30000)
   return render(request, 'app/womentopwear.html', {'womentopwears':womentopwears})


# womanbottom
def womenbottomwear(request, data=None):
   if data == None:
      womenbottomwears = Product.objects.filter(category='WB')
   elif data == 'Denim' or data == 'Mufti' or data == 'BeingHuman' or data == 'JackJohn':
      womenbottomwears = Product.objects.filter(category='WB').filter(brand=data)
   elif data == 'Below':
      womenbottomwears = Product.objects.filter(category='WB').filter(discounted_price__lt=10000)
   elif data == 'Above':
      womenbottomwears = Product.objects.filter(category='WB').filter(discounted_price__gt=30000)
   return render(request, 'app/womenbottomwear.html', {'womenbottomwears':womenbottomwears})

def boyswear(request, data=None):
 if data == None:
    boyswears = Product.objects.filter(category='B')

 elif data == 'Denim' or data == 'Mufti' or data == 'BeingHuman' or data == 'JackJohn':
    boyswears = Product.objects.filter(category='B').filter(brand=data)
 
 elif data == 'Below':
    boyswears = Product.objects.filter(category='B').filter(discounted_price__lt=10000)
 
 elif data == 'Above':
    boyswears = Product.objects.filter(category='B').filter(discounted_price__gt=30000)

 return render(request, 'app/boyswear.html', {'boyswears':boyswears})


def girlswear(request, data=None):
 if data == None:
    girlswears = Product.objects.filter(category='G')

 elif data == 'Denim' or data == 'Mufti' or data == 'BeingHuman' or data == 'JackJohn':
    girlswears = Product.objects.filter(category='G').filter(brand=data)
 
 elif data == 'Below':
    girlswears = Product.objects.filter(category='G').filter(discounted_price__lt=10000)
 
 elif data == 'Above':
    girlswears = Product.objects.filter(category='G').filter(discounted_price__gt=30000)

 return render(request, 'app/girlswear.html', {'girlswears':girlswears})




# CHECKOUT DONE VIEW
@login_required
def checkout(request):

   user = request.user
   add = Customer.objects.filter(user=user)
   cart_items = Cart.objects.filter(user=user)
   amount = 0.0
   shipping_amount = 50.0
   total_amount = 0.0
   cart_product = [p for p in Cart.objects.all() if p.user == request.user]
   if cart_product: 
      for p in cart_product:
         temp_amount = (p.quantity * p.product.discounted_price)
         amount += temp_amount
      total_amount = amount + shipping_amount
   
   return render(request, 'app/checkout.html', {'add':add, 'total_amount':total_amount, 'amount':amount, 'cart_items':cart_items})


# PAYMENT DONE VIEW
@login_required
def payment_done(request):
   
   user = request.user
   custid = request.GET.get('custid')
   print(custid)
   customer = Customer.objects.get(id=custid)
   print(customer)
   cart = Cart.objects.filter(user=user)
   for c in cart:
      OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
      c.delete()
   
   return redirect("orders")

# CUSTOMER REGISTRATION VIEW
class CustomerRegistrationView(View):
    
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})
    
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages .success(request, 'Congratulations..! Registered Successfully.')
            form.save()
        return render(request, 'app/customerregistration.html', {'form':form})


# PROFILE VIEW
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
   
   def get(self, request):

      form = CustomerProfileForm()
      return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})
   
   def post(self, request):

      form = CustomerProfileForm(request.POST)  
      if form.is_valid():
         usr = request.user
         name = form.cleaned_data['name']
         locality = form.cleaned_data['locality']
         city = form.cleaned_data['city']
         state = form.cleaned_data['state']
         zipcode = form.cleaned_data['zipcode']
         reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
         reg.save()
         messages.success(request, 'Congratulations! Profile Updated Successfully')
      
      return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})


# ADDRESS VIEW
def address(request):                                                                                              
   
   add = Customer.objects.filter(user=request.user)
   return render(request, 'app/address.html', {'add':add, 'active':'btn-primary'})
