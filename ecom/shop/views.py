from django.shortcuts import render, redirect, get_object_or_404
from .forms import CategoryInsertForm,ProductInsertForm
from .models import *
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    data = {}
    data['categories'] = Category.objects.all()
    data['products'] = Product.objects.all()
    return render(request, 'public_panel/home.html',data)

def filter(request, cat_id, cat_slug):
    data = {}
    data['categories'] = Category.objects.all()
    category =  Category.objects.get(pk=cat_id)
    data['products'] = Product.objects.filter(category=category)
    data['category'] = category
    return render(request, 'public_panel/filter.html',data)

def viewProduct(request,product_id,product_slug):
    data = {}
    data['categories'] = Category.objects.all()
    product = Product.objects.get(pk=product_id)
    data['products'] = product
    return render(request, 'public_panel/show-product.html',data)

def auth_login(r):
    form = AuthenticationForm(r.POST or None)
    if r.method == "POST":
        username = r.POST.get('username')
        password = r.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(r,user)
            return redirect('home')
        data = {}
        data['form'] = form
        return render(r,'public_panel/includes/login.html',data)
    
def auth_register(r):
    form = UserCreationForm(r.POST or None)
    if r.method =='POST':
        if form.is_valid():
            form.save()
            return redirect(home)
        data = {}
        data['form'] = form
        return render(r,'public_panel/includes/register.html',data)
    
def auth_logout(r):
    logout(r)
    return redirect(auth_login)
@login_required()
def addToCart(request,slug):
    product = get_object_or_404(Product,slug=slug)
    order_item, created = OrderItem.objects.get_or_create(user=request.user, ordered=False,item=product)
    order_qs = Order.objects.filter(user=request.user,ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item=product).exists():
            order_item.qty += 1
            order_item.save()
        else:
            order.items.add(order_item)
    else:
         order = Order.objects.create(user=request.user, ordered=False)
         order.items.add(order_item)
    return redirect(myCart)

@login_required()
def minusToCart(request,slug):
    product = get_object_or_404(Product,slug=slug)
    order_item  = OrderItem.objects.get(user=request.user, ordered=False,item=product)
    order_qs = Order.objects.filter(user=request.user,ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item=product).exists():
            if order_item.qty > 1:
              order_item.qty -= 1
              order_item.save()
            else:
                removeFrom(request, slug)
    return redirect(myCart)

@login_required()
def removeFrom(request,slug):
    product = get_object_or_404(Product,slug=slug)
    order_item = OrderItem.objects.get(user=request.user, ordered=False, item=product)
    if order_item:
        order_item.delete()
    return redirect(myCart)

    

@login_required()
def myCart(request):
    data ={}
    data['order'] = Order.objects.get(user=request.user, ordered=False)
    return render(request, "public_panel/cart.html",data)

# admin views

def dashboard(request):
    return render(request, 'admin-panel/dashboard.html')

def manageCategory(request):
    form = CategoryInsertForm(request.POST or None)
    categories = Category.objects.all()
    if form.is_valid():
        form.save()
        return redirect(manageCategory)
       
    return render(request, 'admin-panel/manage-categories.html',{"form":form, "catgories":categories})


def deleteCategory(request,id):
    category = Category.objects.get(id=id)
    category.delete()
    return redirect(manageCategory)


def manageProduct(request):
    data={}
    data['products'] = Product.objects.all()
    return render(request, 'admin-panel/manage-products.html',data)

def addProduct(request):
    form = ProductInsertForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect(manageProduct)
    return render(request, 'admin-panel/add-product.html',{"form":form})

def deleteProduct(request,id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect(manageProduct)


