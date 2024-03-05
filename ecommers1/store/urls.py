from django.urls import path
from .views import Index, Login, Signup, Logout, Cart, Checkout, Orders
from .middlewares.auth import auth_middleware

urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('signup', Signup.as_view(), name='signuppage'),
    path('login', Login.as_view(), name='loginpage'),
    path('logout', Logout.as_view(), name='logout'),
    path('cart', Cart.as_view(), name='cart'),
    path('checkout', Checkout.as_view(), name='checkout'),
    path('orders', auth_middleware(Orders.as_view()), name='orders'),

]