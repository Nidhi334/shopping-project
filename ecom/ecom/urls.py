
from django.contrib import admin
from django.urls import path
from shop.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("",home, name="public.home"),
    path("filter/<int:cat_id>/<slug:cat_slug>/",filter, name="public.filter"),
    path("show/<int:product_id>/<slug:product_slug>/",viewProduct, name="public.viewProduct"),
    path("cart/",myCart, name="public.cart"),
    path("auth/login/",auth_login, name="public.login"),
    path("auth/register/",auth_register, name="public.register"),
    path("auth/logout/",auth_logout, name="public.logout"),
    path("add-to-cart/<slug:slug>/", addToCart, name="public.add_to_cart"),
    path("minus-to-cart/<slug:slug>/", minusToCart, name="public.minus_to_cart"),
    path("remove-from-cart/<slug:slug>/", removeFrom, name="public.remove_from_cart"),

    # admin url

    path("admin-panel/",dashboard, name="admin.dashboard"),
    path("admin-panel/category", manageCategory, name="admin.category"),
    path("admin-panel/category/<int:id>/delete", deleteCategory, name="admin.category.delete"),
    path("admin-panel/product", manageProduct, name="admin.product"),
    path("admin-panel/product/add", addProduct, name="admin.product.add"),
    path("admin-panel/product/<int:id>/delete", deleteProduct, name="admin.product.delete"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
