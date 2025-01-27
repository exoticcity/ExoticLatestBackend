from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register('getProducts', GetProducts, basename='products')
# router.register('getSalesPrice', GetPrices, basename='getWEBPrices')

urlpatterns = [
    path('create/', UserCreateAPIView.as_view(), name='user-create'),
    path('login/', loginApi, name='loginCustomer'),
    path('createUserBC/', createUserBC, name='createBCUSER'),
    path('update_customer/<str:custNo>/', updateCustomer, name='updatecustomer'),
    path('otpVerification/', otpApi, name='otpVerify'),
    path('user/<customerId>/', GetUserByCustomerIdView.as_view(),
         name='get_user_by_name'),
    path('getCustomersFromBC/', getCustomersFromBC, name='getCustomersFromBC'),
    # path('getBCProducts/', getProductsFromBC, name='getBCProducts'),
    # path('getBCSalesPrice/', getPricesFromBC, name='getBCProducts'),
    path('', include(router.urls)),
    path('forget-password/', forget_password, name='forget_password'),
    path('reset-password/<int:user_id>/<str:token>/', reset_password, name='reset_password'),
    path('deleteUser/<str:user_id>/', deleteUser, name='deleteUser'),
    path('syncCustomerOnWeb/<str:user_id>/', syncCustomerOnWeb, name='syncCustomerOnWeb'),
    path('bcemailvalidation/', bcEmailValidation, name='bcemailvalidation'),
    path('inactiveUserFromWeb/<str:customerNo>/', inactiveUserFromWeb, name='inactiveUserFromWeb'),
    path('changeEmailFromWeb/<str:customerNo>/<str:email>/', changeEmailFromWeb, name='changeEmailFromWeb'),
]
