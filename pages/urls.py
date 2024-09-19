from django.urls import path
from .views import homePageView, AboutPageView, ContactPageView, ProductIndexView, ProductShowView, ProductCreateView, CartView, CartRemoveAllView, ImageViewFactory, ImageViewNoDI
from django.conf import settings
from django.conf.urls.static import static
from .utils import ImageLocalStorage
urlpatterns = [
    path("", homePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("contact/", ContactPageView.as_view(), name="contact"),
    path("products/", ProductIndexView.as_view(), name="index"),
    path("products/create", ProductCreateView.as_view(), name="form"),
    path("products/<str:id>", ProductShowView.as_view(), name="show"),
    path("cart/",  CartView.as_view(), name="cart_index"),
    path("cart/add/<int:product_id>", CartView.as_view(), name="cart_add"),
    path("cart/removeAll", CartRemoveAllView.as_view(), name="cart_removeAll"),
    path("image/", ImageViewFactory(ImageLocalStorage()).as_view(), name="image_index"),
    path('image/save', ImageViewFactory(ImageLocalStorage()).as_view(), name='image_save'),
    path('imagenotdi/', ImageViewNoDI.as_view(), name='imagenodi_index'),
    path('imagenotdi/save', ImageViewNoDI.as_view(), name='imagenodi_save'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    