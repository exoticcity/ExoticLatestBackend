from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.http import JsonResponse
import requests
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
import base64
from django.core.files.base import ContentFile
from django.db.models import Q
import os
# Create your views here.

def getToken():
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
        raise ValidationError('Unable to get access token')
    return {"Authorization" : f"Bearer {access_token}"}

def updateJobs():
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
                        # 'LastDateTimeModified': item['LastDateTimeModified'],
                        # Storing picture in the image field
                        # 'Picture': base64_image['picture']
                    }
                )
            print(created)
        return JsonResponse({'message': "Products Updated!"})
 
    return JsonResponse({'message': "Products Updated!"})

def updateItemsalepriceJobs():
    time = 0
    current_datetime = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=36)
    formatted_datetime = current_datetime.strftime(
        "%Y-%m-%dT%H:%M:%S.%f")[:-5] + "Z"
    try:
        time = LastTimeUpdation.objects.latest('timeStamp').timeStamp
    except:
        pass
 
    if time != 0:
        lastUpdatedTime = time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    else:
        lastUpdatedTime = formatted_datetime
    
    print(lastUpdatedTime)
    price_url = f"https://api.businesscentral.dynamics.com/v2.0/7c885fa6-8571-4c76-9e28-8e51744cf57a/Live/ODataV4/Company('My%20Company')/itemsaleprice?$filter=ModifedDateTime gt {lastUpdatedTime}"
    response = requests.get(price_url, headers=getToken())
 
    if response.status_code == 200:
        price_data = response.json()
        for price in price_data['value']:
            SalesPrice.objects.update_or_create(
                Srno=f"{price['salestype']}-{price['Salecode']}-{price['ItemNo']}-{price['MinimumQuantity']}",
                defaults={
                    'salestype': price['salestype'],
                    'Salecode': price['Salecode'],
                    'ItemNo': price['ItemNo'],
                    'UnitPrice': price['UnitPrice'],
                    'MinimumQuantity': price['MinimumQuantity'],
                    'StartDate': price['StartDate'],
                    'EndDate': price['EndDate'],
                    'SystemModifiedAt': price['ModifedDateTime']
                }
            )
        print('Prices updated!')
 
    LastTimeUpdation.objects.create(timeStamp=formatted_datetime)
    
    return JsonResponse({'message': 'Products and Prices Updated!'})