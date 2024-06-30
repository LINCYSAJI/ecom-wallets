"""
URL configuration for walletsland project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from wallets import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path("register/",views.RegistrationView.as_view(),name="register"),
    
    path("",views.LoginView.as_view(),name="signin"),
    
    path("index/",views.IndexView.as_view(),name='index'),
    
    path("wallet/detail/<int:pk>/",views.WalletDetailView.as_view(),name="wallet-detail"),
    
    path("wallet/<int:pk>/carts/add",views.AddToCartView.as_view(),name="addto-cart"),
    
    path("carts/all/",views.CartSummaryView.as_view(),name="cart-summary"),
    
    path("basketitem/<int:pk>/remove/",views.CartDelete.as_view(),name="cart-delete"),
    
    path("signout/",views.SignOutView.as_view(),name="signout"),
    
    path("basketitem/quantity/<int:pk>/change/",views.cartQuantityUpadateView.as_view(),name="quantity-update"),
    
    path("order/",views.OrderPlaceView.as_view(),name="place-order"),
    
    path("order/summary/",views.OrderSummaryView.as_view(),name="order_summary")
    
    
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
