from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('getProducts', GetProducts, basename='products')
router.register('getSalesPrice', GetPrices, basename='getWEBPrices')
router.register('getBrands', GetBrands, basename='getWEBBrands')
router.register('cart', CartAPIViewset, basename='cartApi')
router.register('getCategories', GetCategory, basename='getWEBCategories')

urlpatterns = [
    path('getAccessToken/', get_access_token, name='get_access_token'),
    path('getPrice/<str:ItemNo>/<str:group>/<int:qnty>/', getPrice, name='get_price'),
    path('getBCProducts/', getProductsFromBC, name='getBCProducts'),
    path('getBCSalesPrice/', getPricesFromBC, name='getBCProducts'),
    path('', include(router.urls)),
    path('update_item_bulk/', updateItemBulk, name='updateItemBulk'),
    path('update_item/<str:itemNo>/', updateItem, name='updateitem'),
    path('update_cart/<str:pk>/', updateCart, name='updateCart'),
    path('create_cart/', createCart, name='createCart'),
    path('upload/', upload_zip, name='upload_zip'),
]
