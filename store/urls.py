from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns= [
    path('',views.store,name="store"),
    path('store',views.store,name="store"),
    #path('store/<slug>',views.store)
    path('cart',views.CartView,name="cart"),
    path('checkout/',views.checkout_items,name="checkout"),
    path('qcheckout/<slug>',views.Qcheckout,name="quickcheckout"),
    path('items/<slug>',views.items,name="items"),
    path('checkout',views.checkout_items,name="checkoutitems"),
    path('register',views.register,name="register"),
    path('login',views.login,name="login"),
    path('logout',views.logout,name="logout"),
    path('cart/<slug>',views.add_to_cart,name='addtocart'),
    path('removeitem/<slug>',views.decreasecart,name="remove from cart"),
    path('payment_gateway',views.payment_gateway,name="payment"),
    path('address',views.address,name="addaddress"),
    path('myorders',views.myorders,name="myorders"),
    path('seller',views.seller,name="seller")
]


urlpatterns = urlpatterns + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
