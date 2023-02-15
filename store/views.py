from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import  Product,Order,Cart,Persondetails,Ordered
from django.contrib import messages
from django.contrib.auth.models import User,auth
import time
from datetime import datetime
# Create your views here

def Qcheckout(request,slug):
    if request.user.is_authenticated:
        item = get_object_or_404(Product,slug=slug)
        #print(item)
        order_item,created= Cart.objects.get_or_create(
        item = item,
        user= request.user,
        purchased=False
        )
        order_qs= Order.objects.filter(user=request.user,ordered=False)

        if order_qs.exists():
           order = order_qs[0]

           if order.orderitems.filter(item__slug=item.slug,purchased=False).exists():

                order_item.quantity+=1
                order_item.save()
                #messages.info(request,"Item Updated To Cart")
                return redirect('checkout')
           else:
               order.orderitems.add(order_item)
               #messages.info(request,"Item added to cart")
               return redirect('checkout')


        else:

           order= Order.objects.create(user=request.user,ordered=False)

           order.orderitems.add(order_item)

          # messages.info(request,"This item was added to your cart.")
           return redirect('checkout')



    else:
       return redirect('login')










#add to cart_tag

def add_to_cart(request,slug):
    if request.user.is_authenticated:


         #messages.info(request,'hey yo')
         #return redirect('/')
         item = get_object_or_404(Product,slug=slug)
         #print(item)
         order_item,created= Cart.objects.get_or_create(
         item = item,
         user= request.user,
         purchased=False
         )

         order_qs= Order.objects.filter(user=request.user,ordered=False)

         if order_qs.exists():
            order = order_qs[0]

            if order.orderitems.filter(item__slug=item.slug,purchased=False).exists():

                 order_item.quantity+=1
                 order_item.save()
                 messages.info(request,"Item Updated To Cart")
                 return redirect('/')
            else:
                order.orderitems.add(order_item)
                messages.info(request,"Item added to cart")
                return redirect('/')


         else:

            order= Order.objects.create(user=request.user,ordered=False)

            order.orderitems.add(order_item)

            messages.info(request,"This item was added to your cart.")
            return redirect('/')



    else:
        return redirect('login')













def store(request):

    if request.method=="POST":
        sl =[]
        search = request.POST['search']
        for s in  Product.objects.all():
            if(search in s.heading):
                sl.append(Product.objects.all().filter(slug=s.slug))
            else:
                messages.info(request,"No product found")


        return render(request,'store/store.html',{'context':sl})

    else:
        context= Product.objects.all()

        return render(request,'store/store.html',{'context':context})








def items(request,slug):
    context= Product.objects.get(slug=slug)
    return render(request,'store/itemdetails.html',{'context':context})

def checkout_items(request):
     if request.user.is_authenticated:
        user= request.user


        carts= Cart.objects.filter(user=user,purchased=False)
        orders= Order.objects.filter(user=user,ordered=False)
        if carts.exists():

             order = orders[0]
             address= Persondetails.objects.filter(user=user)
             if address:
                 add=address[0]
                 return render(request,'store/checkout.html',{"carts":carts,'order':order,'add':add})

             else:
                 return redirect('/address')

     else:
         return redirect('/login')



def register(request):
    if request.method== 'POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        pwd1=request.POST['pwd1']
        pwd2= request.POST['pwd2']
        if pwd1==pwd2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'email is already in use')
                return redirect('register')

            else:
                user = User.objects.create_user(username=email,password=pwd1,email=email,first_name=first_name,last_name=last_name)
                user.save()
                return redirect('/login')

        else:
            messages.info(request,'password not matched')
            return redirect('register')

    else:
        return render(request,'store/register.html')

def login(request):
    if  request.method== 'POST':
        username = request.POST['email']
        pwd= request.POST['pwd']

        user = auth.authenticate(username=username,password=pwd)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')
           

    else:
         return render(request,'store/login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def CartView(request):
    if request.user.is_authenticated:
        user= request.user

        carts= Cart.objects.filter(user=user,purchased=False)
        orders= Order.objects.filter(user=user,ordered=False)


        if carts.exists():

             order = orders[0]
             print(orders)
             return render(request,'store/cart.html',{"carts":carts,'order':order})



        else:
            messages.warning(request,"You don't have an active order")
            return  redirect('/')



    else:
        return redirect('login')


def decreasecart(request,slug):
    item= get_object_or_404(Product,slug=slug)
    order_qs = Order.objects.filter(
        user= request.user,
        ordered= False
    )

    if order_qs.exists():
        order= order_qs[0]
        if order.orderitems.filter(item__slug=item.slug).exists():
            order_item= Cart.objects.filter(
                item= item,
                user=request.user
            )[0]
            if order_item.quantity>1:
                order_item.quantity-= 1
                order_item.save()

            else:
                order.orderitems.remove(order_item)
                order_item.delete()

            messages.info(request,f"{item.heading} quantity has updated")
            return redirect('cart')

        else:
            messages.info(request,f"{item.name} quantity has updated")
            return redirect('cart')

    else:
        messages.info(request,"you don't have an active order")
        return redirect('cart')



def payment_gateway(request):
    user=request.user
    order= Order.objects.get(user=user,ordered=False)
    order.ordered=True
    order.created = datetime.now()
    order.save()
    cartItems = Cart.objects.filter(user=user,purchased="False")
    for item in cartItems:
        item.purchased = True
        item.save()
    #ordered = Ordered.objects.create(user=user,orderitems=)
    return render(request,'store/payment_gateway.html')
    #time.sleep(7)
    #return redirect('/')

def address(request):
    user= request.user
    if request.method == "POST":
        name=request.POST['name']
        email=request.POST['email']
        address=request.POST['address']
        city=request.POST['city']
        zip=request.POST['zipcode']
        country=request.POST['country']
        state=request.POST['state']
        Persondetails.objects.create(user=user,email=email,address=address,
        city=city,zipcode=zip,state=state,country=country)
        return redirect('checkout')

    if request.user.is_authenticated:
        user=request.user
        add=Persondetails.objects.filter(user=user)
        if(add):
            return redirect('checkout')
        else:
            return render(request,'store/address.html')


def myorders(request):
    user= request.user
    if user.is_authenticated:
        carts= Cart.objects.filter(user=user,purchased=True)
        orders= Order.objects.filter(user=user,ordered=True)


        if carts.exists():
            if orders.exists():
                order = orders[0]
                #print(orders)
                return render(request,'store/myorders.html',{"carts":carts})

            else:
                messages.info(request,"You don't have any  order")
                return  redirect('/')


        else:
            messages.info(request,"you don't have any order")
            return redirect('/')
    else:
        return redirect('login')


def seller(request):
    user = request.user
    if user.is_authenticated:
       # messages.info(request,user.password)
        if user.email == "jatinecomm@gmail.com":
            carts= Cart.objects.filter(purchased=True)
            orders= Order.objects.filter(ordered=True)
            if carts.exists():
                 if orders.exists():
                     order = orders[0]
                     return render(request,'store/seller.html',{"order":order,"carts":carts})
                 else:
                     order =''    
            else:
                 return HttpResponse('<h2>No active order <a href="/">Go to Home Page </a> </h2>')     

        else:
             return HttpResponse('<h2>The page you are looking for does not exist <a href="/">Go to Home Page </a> </h2>')     
              
    else:
        return HttpResponse('<h2>The page you are looking for does not exist <a href="/">Go to Home Page </a> </h2>')


     

     

     
