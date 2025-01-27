from django.shortcuts import render
from django.http import JsonResponse
import requests
from .token import getToken
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
import base64
from rest_framework import status
from customer.models import *
from django.core.files.base import ContentFile
from django.db.models import Q
from rest_framework.validators import ValidationError
import datetime
from django.shortcuts import get_object_or_404
import math
import os
# from django.core.files.images import Image
# Create your views here.


def get_access_token(request):
    access_token = None
    data = {
        'grant_type': 'client_credentials',
        'client_id': 'a8391b9c-4583-46c3-a449-a0de6e199161',
        'client_secret': os.environ.get('CLIENT_SECRET'),
        'scope': 'https://api.businesscentral.dynamics.com/.default'
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(
        'https://login.microsoftonline.com/7c885fa6-8571-4c76-9e28-8e51744cf57a/oauth2/v2.0/token',
        data=data,
        headers=headers
    )
    if response.status_code == 200:
        token = response.json()
        access_token = token['access_token']
    else:
        return JsonResponse({'error': 'Internal Server Error'}, status=500)
    return JsonResponse({'access_token': access_token})


def getProductsFromBC(request, *args, **kwargs):
    url = "https://api.businesscentral.dynamics.com/v2.0/7c885fa6-8571-4c76-9e28-8e51744cf57a/Live/ODataV4/Company(%27My%20Company%27)/itemApi?$filter = Type eq 'Inventory'"
    while url:
        response = requests.get(url, headers=getToken())
        if response.status_code == 200:
            data = response.json()
            for item in data['value']:
                # print(item["ItemNo"])
                # imgurl = f"https://api.businesscentral.dynamics.com/v2.0/7c885fa6-8571-4c76-9e28-8e51744cf57a/Live/ODataV4/Company(%27My%20Company%27)/itempic?$filter=ItemNo eq '{item['ItemNo']}'"
                # response = requests.get(imgurl, headers=getToken())
                # print(imgurl)
                # print(response.status_code)
                # if response.status_code == 200:
                #     img = response.json()
                #     if 'value' in img and img['value'] and img['value'][0]:
                #         print(img['value'][0])
                #         if img['value'][0]:
                #             base64_image = img['value'][0]
                            # print(base64_image['picture'])
                product, created = Product.objects.update_or_create(
                    ItemNo=item['ItemNo'],
                    defaults={
                        'Description': item['Description'],
                        'Blocked': item['Blocked'],
                        'SearchDescription': item['SearchDescription'],
                        'BaseUnitOfMeasure': item['BaseUnitOfMeasure'],
                        'ParentCategory': item['ParentCategory'].replace("&", ""),
                        'ItemCategoryCode': item['ItemCategoryCode'].replace("&", ""),
                        'ItemSubCategoryCode': item['ItemSubCategoryCode'].replace("&", ""),
                        'Brand': item['Brand'].replace("&", ""),
                        'NetWeight': item['NetWeight'],
                        'vat': item['VAT'],
                        'Packaging': item['Packaging'],
                        'BarCode': item['BarCode'],
                        'SalesUnitOfMeasure': item['SalesUnitOfMeasure'],
                        'WeightDescription': item['WeightDescription'],
                        'Type': item['Type'],
                        'Quantity': item['Quantity'],
                        'BrandLink': item['BrandLink'],
                        'GTIN': item['GTIN'],
                        'PurchasingCode': item['PurchasingCode'],
                        'LastDateTimeModified': item['LastDateTimeModified'],
                        'SalesBlocked': item['SalesBlocked']
                        # Storing picture in the image field
                        # 'Picture': base64_image['picture']
                    }
                )
            return JsonResponse({'message': "Products Created!"})

    return JsonResponse({'message': "Products Created!"})


def getPricesFromBC(request, *args, **kwargs):
    url = "https://api.businesscentral.dynamics.com/v2.0/7c885fa6-8571-4c76-9e28-8e51744cf57a/Live/ODataV4/Company('My%20Company')/itemsaleprice?$filter=ModifedDateTime gt 2024-10-04 15:51:51.305+00"
    nextUrl = True

    while nextUrl:
        # try:
            response = requests.get(url, headers=getToken())
            if response.status_code == 200:
                real_data = response
                data = response.json()

                for item in data['value']:
                    SalesPrice.objects.update_or_create(
                        Srno = f"{item['salestype']}-{item['Salecode']}-{item['ItemNo']}-{item['MinimumQuantity']}",
                        defaults={
                            'salestype': item['salestype'],
                            'Salecode': item['Salecode'],
                            'ItemNo': item['ItemNo'],
                            'UnitPrice': item['UnitPrice'],
                            'MinimumQuantity': item['MinimumQuantity'],
                            'StartDate': item['StartDate'],
                            'EndDate': item['EndDate'],
                            'SystemModifiedAt': item['ModifedDateTime']
                        }
                    )
                if real_data.json()["@odata.nextLink"]:
                    url = real_data.json()["@odata.nextLink"]
                    print(url)
                else:
                    nextUrl = False
                    return JsonResponse({'transformed_data': "created"})

        # except requests.exceptions.RequestException as e:
        #     return JsonResponse({'error': 'Connection aborted.'}, status=500)

    return JsonResponse({'transformed_data': "Created"})
    
    
    
def updatePricesFromBC(lastUpdatedTime):

    url = f"https://api.businesscentral.dynamics.com/v2.0/7c885fa6-8571-4c76-9e28-8e51744cf57a/Live/ODataV4/Company('My%20Company')/itemsaleprice?$filter=ModifedDateTime gt {lastUpdatedTime}"
    nextUrl = True

    while nextUrl:
        # try:
            response = requests.get(url, headers=getToken())
            if response.status_code == 200:
                print(200)
                real_data = response
                data = response.json()

                for item in data['value']:
                    print(item)
                    SalesPrice.objects.update_or_create(
                        Srno = f"{item['salestype']}-{item['Salecode']}-{item['ItemNo']}-{item['MinimumQuantity']}",
                        defaults={
                            'salestype': item['salestype'],
                            'Salecode': item['Salecode'],
                            'ItemNo': item['ItemNo'],
                            'UnitPrice': item['UnitPrice'],
                            'MinimumQuantity': item['MinimumQuantity'],
                            'StartDate': item['StartDate'],
                            'EndDate': item['EndDate'],
                            'SystemModifiedAt': item['ModifedDateTime']
                        }
                    )
                real_data_response = real_data.json()  # Assuming real_data is a response object
                if "@odata.nextLink" in real_data_response:
                    url = real_data_response["@odata.nextLink"]
                else:
                    nextUrl = False
                    # return JsonResponse({'transformed_data': "created"})

        # except requests.exceptions.RequestException as e:
        #     return JsonResponse({'error': 'Connection aborted.'}, status=500)

    # return JsonResponse({'transformed_data': "Created"})

class GetProducts(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = [
        'ItemNo',
        'Description',
        'SearchDescription',
        'ParentCategory',
        'ItemCategoryCode',
        'ItemSubCategoryCode',
        'Brand',
        'BarCode'
    ]
    pagination_class = LimitOffsetPagination
    search_fields = [
        'ItemNo',
        'Description',
        'SearchDescription',
        'ParentCategory',
        'ItemCategoryCode',
        'ItemSubCategoryCode',
        'Brand',
        'BarCode'
    ]

    def get_queryset(self):
        return Product.objects.all()

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)  # get the built-in response
        queryset = self.filter_queryset(self.get_queryset())
        
        # get the distinct values
        # ParentCategory = queryset.order_by().values_list('ParentCategory', flat=True).distinct()
        ItemCategoryCode = list(filter(None, queryset.order_by().values_list(
                    'ItemCategoryCode', flat=True).distinct()))
        ItemSubCategoryCode = list(filter(None, queryset.order_by().values_list(
            'ItemSubCategoryCode', flat=True).distinct()))
        Brand = list(filter(None, Product.objects.all().order_by().values_list('Brand', flat=True).distinct()))
        if '?' in self.request.get_full_path():
            filters_list = self.request.get_full_path().split('?')[1].split('&')
            for f in filters_list:
                print(f.split('=')[0])
                ptCat=''
                itCat=''
                if f.split('=')[0] == 'ParentCategory':
                    ptCat=f.split('=')[1]
                    ItemCategoryCode = list(filter(None, Product.objects.filter(ParentCategory=f.split('=')[1].replace('%20', ' ')).order_by().values_list(
                        'ItemCategoryCode', flat=True).distinct()))
                    Brand = list(filter(None, Product.objects.filter(Q(ParentCategory=f.split('=')[1].replace('%20', ' '))).order_by().values_list('Brand', flat=True).distinct()))
                    ItemSubCategoryCode = list(filter(None, Product.objects.filter(Q(ParentCategory=f.split('=')[1].replace('%20', ' '))).order_by().values_list(
                'ItemSubCategoryCode', flat=True).distinct()))
                        
                if f.split('=')[0] == 'ItemCategoryCode':
                    itCat=f.split('=')[1]
                    ItemSubCategoryCode = list(filter(None, Product.objects.filter(Q(ItemCategoryCode=f.split('=')[1].replace('%20', ' '))).order_by().values_list(
                'ItemSubCategoryCode', flat=True).distinct()))
                    Brand = list(filter(None, Product.objects.filter(Q(ItemCategoryCode=f.split('=')[1].replace('%20', ' '))).order_by().values_list('Brand', flat=True).distinct()))
                
                
                if f.split('=')[0] == 'ItemSubCategoryCode':
                    Brand = list(filter(None, Product.objects.filter(Q(ItemSubCategoryCode=f.split('=')[1].replace('%20', ' '))).order_by().values_list('Brand', flat=True).distinct()))

        # create a new dictionary for the response data
        data = {
            'results': response.data,
            'distinct_ItemCategoryCode': ItemCategoryCode,
            'distinct_ItemSubCategoryCode': ItemSubCategoryCode,
            'distinct_Brand': Brand,
        }
        # create a new Response object with the new data
        return Response(data)

    # def get(self, request, *args, **kwargs):
    #     products = self.get_queryset()
    #     serializer = self.get_serializer(products, many=True)
    #     return JsonResponse({"data": serializer.data}, status=200)


class GetBrands(viewsets.ViewSet):
    def list(self, request):
        brands = Product.objects.values_list('Brand', flat=True).distinct()
        return JsonResponse({'brands': list(brands)})


class GetPrices(viewsets.ModelViewSet):
    serializer_class = PriceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = "__all__"
    pagination_class = LimitOffsetPagination
    search_fields = "__all__"

    def get_queryset(self):
        return SalesPrice.objects.all()

    def get(self, request, *args, **kwargs):
        prices = self.get_queryset()
        serializer = self.get_serializer(prices, many=True)
        return JsonResponse({"data": serializer.data}, status=200)


class GetCategory(viewsets.ViewSet):
    def list(self, request):
        brands = Product.objects.values_list('Brand', flat=True).distinct()
        return JsonResponse({'brands': list(brands)})
        
def getPrice(self, ItemNo, group, qnty):
    Price = 0
    try:
        items = SalesPrice.objects.filter(ItemNo=ItemNo)
        for item in items:
            if 'Campaign' in item.salestype and item.EndDate >= datetime.date.today():
                filteredPrice = SalesPrice.objects.filter(ItemNo=ItemNo, salestype='Campaign').first()
                if filteredPrice:
                    Price = filteredPrice.UnitPrice
                else:
                    return JsonResponse({'error': 'Campaign price not found!'})
            else:
                filteredPrice = SalesPrice.objects.filter(ItemNo=ItemNo, Salecode=group, MinimumQuantity__lte=qnty).order_by('MinimumQuantity').last()
                if filteredPrice:
                    Price = filteredPrice.UnitPrice
                else:
                    return JsonResponse({'error': 'Regular price not found!'})
    except Exception as e:
        return JsonResponse({'error': 'Product Not Found! - ' + str(e)})
    
    return JsonResponse({'price': filteredPrice.UnitPrice})

def updateItem(self, itemNo):
    try:
        url = f"https://api.businesscentral.dynamics.com/v2.0/7c885fa6-8571-4c76-9e28-8e51744cf57a/Live/ODataV4/Company(%27My%20Company%27)/itemApi?$filter = ItemNo eq '{itemNo}'"
        response = requests.get(url, headers=getToken())
        print(url)
        print(response)
        if response.status_code == 200:
            data = response.json()
            for item in data['value']:
                print(item)
                product, created = Product.objects.update_or_create(
                        ItemNo=item['ItemNo'],
                        defaults={
                            'Description': item['Description'],
                            'Blocked': item['Blocked'],
                            'SearchDescription': item['SearchDescription'],
                            'BaseUnitOfMeasure': item['BaseUnitOfMeasure'],
                            'ParentCategory': item['ParentCategory'].replace("&", ""),
                            'ItemCategoryCode': item['ItemCategoryCode'].replace("&", ""),
                            'ItemSubCategoryCode': item['ItemSubCategoryCode'].replace("&", ""),
                            'Brand': item['Brand'].replace("&", ""),
                            'NetWeight': item['NetWeight'],
                            'vat': item['VAT'],
                            'Packaging': item['Packaging'],
                            'BarCode': item['BarCode'],
                            'SalesUnitOfMeasure': item['SalesUnitOfMeasure'],
                            'WeightDescription': item['WeightDescription'],
                            'Type': item['Type'],
                            'Quantity': item['Quantity'],
                            'BrandLink': item['BrandLink'],
                            'GTIN': item['GTIN'],
                            'PurchasingCode': item['PurchasingCode'],
                            'LastDateTimeModified': item['LastDateTimeModified'],
                            'SalesBlocked': item['SalesBlocked']
                            # Storing picture in the image field
                            # 'Picture': base64_image['picture']
                        }
                    )
            priceurl = f"https://api.businesscentral.dynamics.com/v2.0/7c885fa6-8571-4c76-9e28-8e51744cf57a/Live/ODataV4/Company('My%20Company')/itemsaleprice?$filter=ItemNo eq '{itemNo}'"
            # nextUrl = True
        
            # while nextUrl:
                # try:
            response = requests.get(priceurl, headers=getToken())
            if response.status_code == 200:
                real_data = response
                data = response.json()

                for item in data['value']:
                    SalesPrice.objects.update_or_create(
                        Srno = f"{item['salestype']}-{item['Salecode']}-{item['ItemNo']}-{item['MinimumQuantity']}",
                        defaults={
                            'salestype': item['salestype'],
                            'Salecode': item['Salecode'],
                            'ItemNo': item['ItemNo'],
                            'UnitPrice': item['UnitPrice'],
                            'MinimumQuantity': item['MinimumQuantity'],
                            'StartDate': item['StartDate'],
                            'EndDate': item['EndDate'],
                            'SystemModifiedAt': item['ModifedDateTime']
                        }
                    )
                        # if real_data.json()["@odata.nextLink"]:
                        #     url = real_data.json()["@odata.nextLink"]
                        #     print(url)
                        # else:
                        #     nextUrl = False
                        #     return JsonResponse({'transformed_data': "created"})
        
                # except requests.exceptions.RequestException as e:
                #     return JsonResponse({'error': 'Connection aborted.'}, status=500)
        
            return JsonResponse({"success": "Product Updated"})
        else:
            return JsonResponse({"error": "Product Not Found"})

    except Exception as e:
        return JsonResponse({"error": e})

def updateItemBulk(self):
    time = 0
    current_datetime = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=36)
    formatted_datetime = current_datetime.strftime(
        "%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
 
    try:
        time = LastTimeUpdation.objects.latest('timeStamp').timeStamp
    except:
        pass
    if time != 0:
        lastUpdatedTime = time.strftime(
            "%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    else:
        lastUpdatedTime = formatted_datetime
    print(lastUpdatedTime)
    url = f"https://api.businesscentral.dynamics.com/v2.0/7c885fa6-8571-4c76-9e28-8e51744cf57a/Live/ODataV4/Company(%27My%20Company%27)/itemApi?$filter = LastDateTimeModified gt {lastUpdatedTime}"
    print(url)
    response = requests.get(url, headers=getToken())
    print(response)
    LastTimeUpdation.objects.create(
        timeStamp=formatted_datetime
    )
    if response.status_code == 200:
        data = response.json()
        for item in data['value']:
            print(item)
            product, created = Product.objects.update_or_create(
                    ItemNo=item['ItemNo'],
                    defaults={
                        'Description': item['Description'],
                        'Blocked': item['Blocked'],
                        'SearchDescription': item['SearchDescription'],
                        'BaseUnitOfMeasure': item['BaseUnitOfMeasure'],
                        'ParentCategory': item['ParentCategory'].replace("&", ""),
                        'ItemCategoryCode': item['ItemCategoryCode'].replace("&", ""),
                        'ItemSubCategoryCode': item['ItemSubCategoryCode'].replace("&", ""),
                        'Brand': item['Brand'].replace("&", ""),
                        'NetWeight': item['NetWeight'],
                        'vat': item['VAT'],
                        'Packaging': item['Packaging'],
                        'BarCode': item['BarCode'],
                        'SalesUnitOfMeasure': item['SalesUnitOfMeasure'],
                        'WeightDescription': item['WeightDescription'],
                        'Type': item['Type'],
                        'Quantity': item['Quantity'],
                        'BrandLink': item['BrandLink'],
                        'GTIN': item['GTIN'],
                        'PurchasingCode': item['PurchasingCode'],
                        'LastDateTimeModified': item['LastDateTimeModified'],
                        # Storing picture in the image field
                        # 'Picture': base64_image['picture']
                    }
                )
            updatePricesFromBC(lastUpdatedTime)
        return JsonResponse({'message': "Products Updated!"})
 
    return JsonResponse({'message': "Products Updated!"})


# def updateItemBulk(self):
    # lastdatetime = LastDateTime.objects.last()
    # print(lastdatetime.LastDateTimeModified)
    # url = f"https://api.businesscentral.dynamics.com/v2.0/7c885fa6-8571-4c76-9e28-8e51744cf57a/Live/ODataV4/Company(%27My%20Company%27)/itemApi?$filter = LastDateTimeModified eq '{lastdatetime.LastDateTimeModified}'"
    # print(url)
    # response = requests.get(url, headers=getToken())
    # if Product.objects.filter(ItemNo=itemNo).exists():
    #     product = Product.objects.get(ItemNo=itemNo)
    #     product.Description = response.json()['value'][0]['Description']
    #     product.Blocked = response.json()['value'][0]['Blocked']
    #     product.SearchDescription = response.json()['value'][0]['SearchDescription']
    #     product.BaseUnitOfMeasure = response.json()['value'][0]['BaseUnitOfMeasure']
    #     product.ParentCategory = response.json()['value'][0]['ParentCategory']
    #     product.ItemCategoryCode = response.json()['value'][0]['ItemCategoryCode']
    #     product.ItemSubCategoryCode = response.json()['value'][0]['ItemSubCategoryCode']
    #     product.Brand = response.json()['value'][0]['Brand']
    #     product.NetWeight = response.json()['value'][0]['NetWeight']
    #     product.Packaging = response.json()['value'][0]['Packaging']
    #     product.BarCode = response.json()['value'][0]['BarCode']
    #     product.SalesUnitOfMeasure = response.json()['value'][0]['SalesUnitOfMeasure']
    #     product.WeightDescription = response.json()['value'][0]['WeightDescription']
    #     product.Type = response.json()['value'][0]['Type']
    #     product.vat = response.json()['value'][0]['VAT']
    #     product.Quantity = response.json()['value'][0]['Quantity']
    #     product.BrandLink = response.json()['value'][0]['BrandLink']
    #     product.GTIN = response.json()['value'][0]['GTIN']
    #     product.PurchasingCode = response.json()['value'][0]['PurchasingCode']
    #     product.LastDateTimeModified = response.json()['value'][0]['LastDateTimeModified']
    #     product.save()
    #     return JsonResponse({"success": "Product Updated"})
    # else:
    #     return JsonResponse({"error": "Product Not Found"})

def getFuncPrice(ItemNo, group, qnty):
    Price = 0
    try:
        items = SalesPrice.objects.filter(ItemNo=ItemNo)
        for item in items:
            if 'Campaign' in item.salestype and item.EndDate >= datetime.date.today():
                filteredPrice = SalesPrice.objects.filter(ItemNo=ItemNo, salestype='Campaign').first()
                if filteredPrice:
                    Price = filteredPrice.UnitPrice
                else:
                    return JsonResponse({'error': 'Campaign price not found!'})
            else:
                filteredPrice = SalesPrice.objects.filter(ItemNo=ItemNo, Salecode=group, MinimumQuantity__lte=qnty).order_by('MinimumQuantity').last()
                if filteredPrice:
                    Price = filteredPrice.UnitPrice
                else:
                    return JsonResponse({'error': 'Regular price not found!'})
    except Exception as e:
        return JsonResponse({'error': 'Product Not Found! - ' + str(e)})
    
    return {'price': filteredPrice.UnitPrice}

class CartAPIViewset(viewsets.ViewSet):

    def list(self, request):
        queryset = Cart.objects.all()
        serializer = CartSerializer(queryset, many=True)
        return Response(serializer.data)

    # def create(self, request):
    #     try:
    #         customer = Customer.objects.get(customer_id=request.data['customer'])
    #         items = request.data['items_in_cart']
    #         try:
    #             cart = Cart.objects.create(
    #                 customer = customer,
    #                 date_time_created = datetime.datetime.today()
    #             )
    #             cart_amount_including_vat = 0
    #             cart_amount_excluding_vat = 0
    #             cart_vat_amount = 0
    #             if cart:
    #                 for item in items:
    #                     item_created = CartItem.objects.create(
    #                         cart= cart,
    #                         product = Product.objects.get(ItemNo=item["itemNo"]),
    #                         vat_rate = Product.objects.get(ItemNo=item["itemNo"]).vat,
    #                         quantity = item["quantity"]
    #                     )
    #                     response = requests.get(f'https://exoticcity-a0dfd0ddc0h2h9hb.northeurope-01.azurewebsites.net/items/getPrice/{Product.objects.get(ItemNo=item["itemNo"]).ItemNo}/{Customer.objects.get(customer_id=request.data["customer"]).CustomerPriceGroup}/{item_created.quantity}')
    #                     data = response.json()
    #                     item_created.total_amount_excluding_vat = round(round(float(data['price']), 2) * item_created.quantity , 2)
    #                     item_created.total_amount_including_vat = round(( ((round(float(data['price']), 2))*((item_created.vat_rate/100)*item_created.quantity)) + (round(round(float(data['price']), 2) * item_created.quantity , 2)) ), 2)
    #                     item_created.save()
    #                     item_created.vat_amount = round((item_created.total_amount_including_vat - item_created.total_amount_excluding_vat) ,2)
    #                     item_created.save()
    #                     cart_amount_including_vat = cart_amount_including_vat + item_created.total_amount_including_vat
    #                     cart_amount_excluding_vat = cart_amount_excluding_vat + item_created.total_amount_excluding_vat
    #                     cart_vat_amount = cart_vat_amount + item_created.vat_amount

    #                 cart.total_amount_including_vat = cart_amount_including_vat
    #                 cart.total_amount_excluding_vat = cart_amount_excluding_vat
    #                 cart.vat_amount = cart_vat_amount
    #                 cart.save()
    #             return Response({"message": "Cart Created Successfully!"}, status=status.HTTP_201_CREATED)
    #         except Exception as e:
    #             return Response({"message": "Cart Already Exists for this Customer! Refresh! If you still facing same issue try contact your administrator!"}, status=status.HTTP_400_BAD_REQUEST) 

    #     except Exception as e:
    #         raise ValidationError(e)


    def retrieve(self, request, pk=None):
        cust= Customer.objects.get(customer_id=pk)
        queryset = Cart.objects.filter(customer=cust)
        item = get_object_or_404(queryset)
        serializer = CartSerializer(item)
        return Response(serializer.data)

    # def update(self, request, pk=None):
    #     try:
    #         cust= Customer.objects.get(customer_id=pk)
    #         queryset = Cart.objects.filter(customer=cust)
    #         cart = get_object_or_404(queryset)
    #         items_to_update = request.data["items_to_update"]
    #         cart_amount_including_vat = 0
    #         cart_amount_excluding_vat = 0
    #         cart_vat_amount = 0
    #         for item in items_to_update:
    #             print(item)
    #             item_created, created = CartItem.objects.update_or_create(
    #                         cart= cart,
    #                         product = Product.objects.get(ItemNo=item["itemNo"]),
    #                         defaults = {
    #                             'vat_rate' : Product.objects.get(ItemNo=item["itemNo"]).vat,
    #                             'quantity' : item["quantity"]
    #                         },
    #                 )
    #             print("OK")
    #             print(Product.objects.get(ItemNo=item["itemNo"]).ItemNo)
    #             print(Customer.objects.get(customer_id=pk).CustomerPriceGroup)
    #             print(item_created.quantity)
    #             response = getFuncPrice(Product.objects.get(ItemNo=item["itemNo"]).ItemNo, Customer.objects.get(customer_id=pk).CustomerPriceGroup, item_created.quantity)
    #             # response = requests.get(f'https://exoticcity-a0dfd0ddc0h2h9hb.northeurope-01.azurewebsites.net/items/getPrice/{Product.objects.get(ItemNo=item["itemNo"]).ItemNo}/{Customer.objects.get(customer_id=pk).CustomerPriceGroup}/{item_created.quantity}')
    #             print(response)
    #             data = response
    #             item_created.total_amount_excluding_vat = round(round(float(data["price"]), 2) * item_created.quantity , 2)
    #             item_created.total_amount_including_vat = round(( ((round(float(data["price"]), 2))*((item_created.vat_rate/100)*item_created.quantity)) + (round(round(float(data["price"]), 2) * item_created.quantity , 2)) ), 2)
    #             item_created.save()
    #             item_created.vat_amount = round((item_created.total_amount_including_vat - item_created.total_amount_excluding_vat) ,2)
    #             item_created.save()
    #         for created in CartItem.objects.filter(cart=cart):
    #             print(created.vat_amount)
    #             cart_amount_including_vat = float(cart_amount_including_vat) + float(created.total_amount_including_vat)
    #             cart_amount_excluding_vat = float(cart_amount_excluding_vat) + float(created.total_amount_excluding_vat)
    #             cart_vat_amount = float(cart_vat_amount) + float(created.vat_amount)

    #         cart.total_amount_including_vat = cart_amount_including_vat
    #         cart.total_amount_excluding_vat = cart_amount_excluding_vat
    #         cart.vat_amount = cart_vat_amount
    #         cart.save()
    #         serializer = CartSerializer(cart)
    #         return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    #     except Exception as e:
    #         return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        cust= Customer.objects.get(customer_id=pk)
        queryset = Cart.objects.filter(customer=cust)
        cart = get_object_or_404(queryset)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


from rest_framework.decorators import api_view
@api_view(['PUT'])
def updateCart(request, pk=None):
        try:
            cust= Customer.objects.get(customer_id=pk)
            queryset = Cart.objects.filter(customer=cust)
            cart = get_object_or_404(queryset)
            items_to_update = request.data["items_to_update"]
            cart_amount_including_vat = 0
            cart_amount_excluding_vat = 0
            cart_vat_amount = 0
            for item in items_to_update:
                print(item)
                item_created, created = CartItem.objects.update_or_create(
                            cart= cart,
                            product = Product.objects.get(ItemNo=item["itemNo"]),
                            defaults = {
                                'vat_rate' : Product.objects.get(ItemNo=item["itemNo"]).vat,
                                'quantity' : item["quantity"]
                            },
                    )
                print("OK")
                print(Product.objects.get(ItemNo=item["itemNo"]).ItemNo)
                print(Customer.objects.get(customer_id=pk).CustomerPriceGroup)
                print(item_created.quantity)
                response = getFuncPrice(Product.objects.get(ItemNo=item["itemNo"]).ItemNo, Customer.objects.get(customer_id=pk).CustomerPriceGroup, item_created.quantity)
                # response = requests.get(f'https://exoticcity-a0dfd0ddc0h2h9hb.northeurope-01.azurewebsites.net/items/getPrice/{Product.objects.get(ItemNo=item["itemNo"]).ItemNo}/{Customer.objects.get(customer_id=pk).CustomerPriceGroup}/{item_created.quantity}')
                print(response)
                data = response
                item_created.total_amount_excluding_vat = round(round(float(data["price"]), 2) * item_created.quantity , 2)
                item_created.total_amount_including_vat = round(( ((round(float(data["price"]), 2))*((item_created.vat_rate/100)*item_created.quantity)) + (round(round(float(data["price"]), 2) * item_created.quantity , 2)) ), 2)
                item_created.save()
                item_created.vat_amount = round((item_created.total_amount_including_vat - item_created.total_amount_excluding_vat) ,2)
                item_created.save()
            for created in CartItem.objects.filter(cart=cart):
                print(created.vat_amount)
                cart_amount_including_vat = float(cart_amount_including_vat) + float(created.total_amount_including_vat)
                cart_amount_excluding_vat = float(cart_amount_excluding_vat) + float(created.total_amount_excluding_vat)
                cart_vat_amount = float(cart_vat_amount) + float(created.vat_amount)

            cart.total_amount_including_vat = cart_amount_including_vat
            cart.total_amount_excluding_vat = cart_amount_excluding_vat
            cart.vat_amount = cart_vat_amount
            cart.save()
            serializer = CartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def createCart(request):
        try:
            customer = Customer.objects.get(customer_id=request.data['customer'])
            items = request.data['items_in_cart']
            try:
                cart = Cart.objects.create(
                    customer = customer,
                    date_time_created = datetime.datetime.today()
                )
                cart_amount_including_vat = 0
                cart_amount_excluding_vat = 0
                cart_vat_amount = 0
                if cart:
                    for item in items:
                        item_created = CartItem.objects.create(
                            cart= cart,
                            product = Product.objects.get(ItemNo=item["itemNo"]),
                            vat_rate = Product.objects.get(ItemNo=item["itemNo"]).vat,
                            quantity = item["quantity"]
                        )
                        # response = requests.get(f'https://exoticbackend.exoticshop.eu/items/getPrice/{Product.objects.get(ItemNo=item["itemNo"]).ItemNo}/{Customer.objects.get(customer_id=request.data["customer"]).CustomerPriceGroup}/{item_created.quantity}')
                        response = getFuncPrice(Product.objects.get(ItemNo=item["itemNo"]).ItemNo, Customer.objects.get(customer_id=request.data["customer"]).CustomerPriceGroup, item_created.quantity)
                        data = response
                        item_created.total_amount_excluding_vat = round(round(float(data["price"]), 2) * item_created.quantity , 2)
                        item_created.total_amount_including_vat = round(( ((round(float(data["price"]), 2))*((item_created.vat_rate/100)*item_created.quantity)) + (round(round(float(data["price"]), 2) * item_created.quantity , 2)) ), 2)
                        item_created.save()
                        item_created.vat_amount = round((item_created.total_amount_including_vat - item_created.total_amount_excluding_vat) ,2)
                        item_created.save()
                        cart_amount_including_vat = cart_amount_including_vat + item_created.total_amount_including_vat
                        cart_amount_excluding_vat = cart_amount_excluding_vat + item_created.total_amount_excluding_vat
                        cart_vat_amount = cart_vat_amount + item_created.vat_amount

                    cart.total_amount_including_vat = cart_amount_including_vat
                    cart.total_amount_excluding_vat = cart_amount_excluding_vat
                    cart.vat_amount = cart_vat_amount
                    cart.save()
                return Response({"message": "Cart Created Successfully!"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"message": f"{e}Cart Already Exists for this Customer! Refresh! If you still facing same issue try contact your administrator!"}, status=status.HTTP_400_BAD_REQUEST) 

        except Exception as e:
            raise ValidationError(e)


# views.py
import zipfile
import os
from io import BytesIO
from django.core.files.base import ContentFile
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
# from .models import Image
from django.conf import settings

@api_view(['POST'])
def upload_zip(request):
    # Check if file exists in the request
    if 'zip_file' not in request.FILES:
        return Response({'error': 'No ZIP file provided'}, status=status.HTTP_400_BAD_REQUEST)

    zip_file = request.FILES['zip_file']

    # Create a temporary directory to store extracted files
    zip_path = os.path.join(settings.MEDIA_ROOT, 'temp_zip')
    if not os.path.exists(zip_path):
        os.makedirs(zip_path)

    try:
        # Unzip the file in the temporary directory
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(zip_path)

        # Loop through the extracted files and store the images in the database
        image_instances = []
        for filename in os.listdir(zip_path):
            file_path = os.path.join(zip_path, filename)

            if os.path.isfile(file_path):
                # Open the image file
                with open(file_path, 'rb') as img_file:
                    image_content = img_file.read()

                    # Save image to Django model
                    image_name = filename.split('.')[0]  # Take the name without extension
                    image_file = ContentFile(image_content, name=filename)

                    # Save image to the model
                    if Product.objects.filter(ItemNo=image_name.split(' - ')[0]).exists():
                        ins = Product.objects.filter(ItemNo=image_name.split(' - ')[0]).first()
                        ins.Picture = image_file
                        ins.save()
                    # image_instance = Image(name=image_name, image=image_file)
                    # image_instance.save()
                    # image_instances.append(image_instance)
                    print(image_name.split(' - ')[0])

                # Optionally, delete the file after saving to the database
                os.remove(file_path)

        # Clean up by removing the temporary directory
        os.rmdir(zip_path)

        # Return the saved images as response
        return Response(
            {'message': 'Images uploaded and stored successfully', 'images': [img.name for img in image_instances]},
            status=status.HTTP_201_CREATED
        )

    except zipfile.BadZipFile:
        return Response({'error': 'Invalid ZIP file'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
