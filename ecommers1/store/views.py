from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .models.product import Product
from .models.category import Category
from .models.custmer import Custmer
from .models.order import Order
from django.views import View
from store.middlewares.auth import auth_middleware


# Create your views here.

class Index(View):

    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity+1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        print(cart)
        return redirect('homepage')



    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart']={}
        products = None
        categories = Category.get_all_categories()
        categoryId = request.GET.get('category')
        if categoryId:
            products = Product.get_all_products_by_categotyid(categoryId)
        else:
            products = Product.get_all_products()
        data = {}
        data['products'] = products
        data['categories'] = categories
       
        return render(request, 'index.html', data)

    

    
class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')
    
    def post(self, request):
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # vaildidations
        value = { 
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }

        error_message = None
        customer = Custmer(first_name=first_name, last_name=last_name, phone=phone, email=email, password=password)

        error_message = self.validateCustomer(customer)
        #saving
        if not error_message:
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('homepage')
        else:
            data = {
                    'error': error_message,
                    'values': value
            }
            return render(request, 'signup.html', data)
        
    def validateCustomer(self, customer):
        error_message = None
        if(not customer.first_name ):
            error_message = "First Name Requied !!"
        
        elif len(customer.first_name) < 4:
            error_message = 'First Name must be 4 char long or more'
        elif not customer.last_name:
            error_message = 'Last Name Requied !!'
        elif len(customer.last_name) < 4:
            error_message = 'Last Name must be 4 char long or more'
        elif not customer.phone:
            error_message = 'Phone number Requied !!'
        elif len(customer.phone) < 10:
            error_message = 'Phone Number must be 10 char long'
        elif not customer.password:
            error_message = 'password is must'
        elif len(customer.password) < 6:
            error_message = 'password must be 6 char long'
        elif customer.isExists():
            error_message = 'Email Address Already Register..'

        return error_message




class Login(View):
    return_url = None
    def get(self, request):
        Login.return_url = request.GET.get('retrun_url')
        return render(request, 'login.html')
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Custmer.get_customer_by_email(email)
        error_massage = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('homepage')
            else:
                error_massage = 'Email or Password invalid'
        else:
            error_massage = 'Email or Password invalid'

       
        return render(request, 'login.html', {'error': error_massage})
    
    
class Logout(View):
    def get(self, request):
        request.session.clear()
        return redirect('loginpage')
    

class Cart(View):
    def get(self, request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        print(products)
        return render(request, 'cart.html', {'products':products})
    
class Checkout(View):

    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        # print(address, phone, customer, cart, products)
        for product in products:
            print(cart.get(str(product.id)))
            order = Order(customer=Custmer(id=customer),product=product,price=product.price,address=address,phone=phone,quantity=cart.get(str(product.id)))
            order.placeOrder()

        request.session['cart'] = {}
        return redirect('cart')
    
class Orders(View):
    def get(self, request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        orders = orders.reverse()
        return render(request, 'orders.html', {'orders':orders})