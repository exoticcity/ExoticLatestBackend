from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
import random
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
import requests
from django.core.cache import cache
from customer.serializers import *
from items.token import getToken
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
import os
from django.urls import reverse 
import json
from django.core.mail import send_mail
from django.conf import settings
User = get_user_model()

# Create your views here.
def forget_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email').lower()
        print(email)
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            reset_link = request.build_absolute_uri(reverse('reset_password', args=[user.pk, token]))
            reset_link = f'https://exoticcity.be/#/customers/reset-password/{user.pk}/{token}/'
            print(reset_link)
        #     mail = mt.Mail(
        #     sender=mt.Address(email="mailtrap@demomailtrap.com", name="Mailtrap Test"),
        #     to=[mt.Address(email="rhaseeb741@gmail.com")],
        #     subject="You are awesome!",
        #     text="Congrats for sending test email with Mailtrap!",
        #     category="Integration Test",
        # )
            subject = "Verify It's you!"
            message = 'Please use the link below to reset your password. If you are unable to see the link, please enable HTML emails in your client.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]

            html_message = """<!DOCTYPE html>
                            <html lang='en'>
                            <head>
                            <meta charset='UTF-8'>
                            <meta name='viewport' content='width=device-width, initial-scale=1.0'>
                            <title>Password Reset</title>
                            <style>
                                    body {{
                                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                                        color: #333;
                                        margin: 0;
                                        padding: 0;
                                        background-color: #f5f5f5;
                                    }}
                            
                                    .container {{
                                        width: 100%;
                                        max-width: 600px;
                                        margin: auto;
                                        background-color: #fff;
                                        border-radius: 10px;
                                        overflow: hidden;
                                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                                    }}
                            
                                    .header {{
                                        background: linear-gradient(90deg, #FF7F2A 0%, #FF7F2A 100%);
                                        color: #fff;
                                        text-align: center;
                                        padding: 10px;
                                    }}
                            
                                    .content {{
                                        padding: 30px;
                                        background-color: #f0f0f0;
                                    }}
                            
                                    .content p {{
                                        font-size: 16px;
                                        line-height: 1.5;
                                        color: #555;
                                    }}
                            
                                    .footer {{
                                        text-align: center;
                                        padding: 20px;
                                        background-color: #f0f0f0;
                                        border-top: 1px solid #ddd;
                                        font-weight: 600;
                                    }}
                            </style>
                            </head>
                            <body>
                            <div class='container'>
                            <div class='header'>
                            <h1>Password Reset</h1>
                            </div>
                            <div class='content'>
                            <p>Hello,</p>
                            <p>You are receiving this email because we received a password reset request for your account.</p>
                            <p>Please click on the button below to reset your password. This password reset link will expire in 30 minutes.</p>
                            <p style='text-align: center;'>
                            <a href='""" + reset_link + """' 
                                            style='background-color: #FF7F2A; color: #fff; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;'>
                                            Reset Password
                            </a>
                            </p>
                            <p>If you did not request a password reset, no further action is required.</p>
                            </div>
                            <div class='footer'>
                            <p>Thank you for choosing our service.</p>
                            </div>
                            </div>
                            </body>
                            </html>"""


            send_mail(subject, message, email_from, recipient_list, html_message=html_message)
            return JsonResponse({'message': "Password reset link sent to your email."})                                                            

def reset_password(request, user_id, token):
       user = User.objects.get(pk=user_id)
       if default_token_generator.check_token(user, token):
           if request.method == 'POST':
               data = json.loads(request.body)
               new_password = data.get('new_password')
               user.set_password(new_password)
               user.save()
               return JsonResponse({'message': "Password reset successfully."})
       return JsonResponse({'message': "Invalid password reset link."})


def getCustomersFromBC(request, *args, **kwargs):
    url = "https://api.businesscentral.dynamics.com/v2.0/Live/api/bctech/demo/v2.0/Companies(f03f6225-081c-ec11-bb77-000d3abcd65f)/customer"
    while url:
        response = requests.get(url, headers=getToken())
        if response.status_code == 200:
            data = response.json()
            for customer in data['value']:
                cust, created = BCCustomer.objects.update_or_create(
                    No=customer['No'],
                    defaults={
                        'Name': customer['Name'],
                        'SearchName': customer['SearchName'],
                        'Name2': customer['Name2'],
                        'Address': customer['Address'],
                        'Address2': customer['Address2'],
                        'City': customer['City'],
                        'Contact': customer['Contact'],
                        'PhoneNo': customer['PhoneNo'],
                        'Blocked': customer['Blocked'],
                        'DocumentSendingProfile': customer['DocumentSendingProfile'],
                        'ShiptoCode': customer['ShiptoCode'],
                        'OurAccountNo': customer['OurAccountNo'],
                        'TerritoryCode': customer['TerritoryCode'],
                        'GlobalDimension1Code': customer['GlobalDimension1Code'],
                        'GlobalDimension2Code': customer['GlobalDimension2Code'],
                        'ChainName': customer['ChainName'],
                        'BudgetedAmount': customer['BudgetedAmount'],
                        'CreditLimitLCY': customer['CreditLimitLCY'],
                        'CustomerPostingGroup': customer['CustomerPostingGroup'],
                        'CurrencyCode': customer['CurrencyCode'],
                        'CustomerPriceGroup': customer['CustomerPriceGroup'],
                        'LanguageCode': customer['LanguageCode'],
                        'RegistrationNumber': customer['RegistrationNumber'],
                        'StatisticsGroup': customer['StatisticsGroup'],
                        'PaymentTermsCode': customer['PaymentTermsCode'],
                        'SalespersonCode': customer['SalespersonCode'],
                        'ShipmentMethodCode': customer['ShipmentMethodCode'],
                        'PlaceofExport': customer['PlaceofExport'],
                        'CustomerDiscGroup': customer['CustomerDiscGroup'],
                        'CountryRegionCode': customer['CountryRegionCode'],
                        'Amount': customer['Amount'],
                        'DebitAmount': customer['DebitAmount'],
                        'CreditAmount': customer['CreditAmount'],
                        'InvoiceAmounts': customer['InvoiceAmounts'],
                        'OtherAmountsLCY': customer['OtherAmountsLCY'],
                        'Comment': customer['Comment'],
                        'LastStatementNo': customer['LastStatementNo'],
                        'Prepayment': customer['Prepayment'],
                        'PartnerType': customer['PartnerType'],
                        'Payments': customer['Payments'],
                        'PostCode': customer['PostCode'],
                        'PrintStatements': customer['PrintStatements'],
                        'PricesIncludingVAT': customer['PricesIncludingVAT'],
                        'ProfitLCY': customer['ProfitLCY'],
                        'BilltoCustomerNo': customer['BilltoCustomerNo'],
                        'Priority': customer['Priority'],
                        'PaymentMethodCode': customer['PaymentMethodCode'],
                        'LastModifiedDateTime': customer['LastModifiedDateTime'],
                        'GlobalDimension1Filter': customer['GlobalDimension1Filter'],
                        'GlobalDimension2Filter': customer['GlobalDimension2Filter'],
                        'Balance': customer['Balance'],
                        'BalanceLCY': customer['BalanceLCY'],
                        'BalanceDue': customer['BalanceDue'],
                        'NetChange': customer['NetChange'],
                        'NetChangeLCY': customer['NetChangeLCY'],
                        'SalesLCY': customer['SalesLCY'],
                        'InvAmountsLCY': customer['InvAmountsLCY'],
                        'InvDiscountsLCY': customer['InvDiscountsLCY'],
                        'NoofInvoices': customer['NoofInvoices'],
                        'InvoiceDiscCode': customer['InvoiceDiscCode'],
                        'InvoiceCopies': customer['InvoiceCopies'],
                        'PmtDiscountsLCY': customer['PmtDiscountsLCY'],
                        'PmtToleranceLCY': customer['PmtToleranceLCY'],
                        'BalanceDueLCY': customer['BalanceDueLCY'],
                        'PaymentsLCY': customer['PaymentsLCY'],
                        'CrMemoAmounts': customer['CrMemoAmounts'],
                        'CrMemoAmountsLCY': customer['CrMemoAmountsLCY'],
                        'FinanceChargeMemoAmounts': customer['FinanceChargeMemoAmounts'],
                        'ShippedNotInvoiced': customer['ShippedNotInvoiced'],
                        'ShippedNotInvoicedLCY': customer['ShippedNotInvoicedLCY'],
                        'ShippingAgentCode': customer['ShippingAgentCode'],
                        'ApplicationMethod': customer['ApplicationMethod'],
                        'LocationCode': customer['LocationCode'],
                        'FaxNo': customer['FaxNo'],
                        'VATBusPostingGroup': customer['VATBusPostingGroup'],
                        'VATRegistrationNo': customer['VATRegistrationNo'],
                        'CombineShipments': customer['CombineShipments'],
                        'GenBusPostingGroup': customer['GenBusPostingGroup'],
                        'GLN': customer['GLN'],
                        'County': customer['County'],
                        'EMail': customer['EMail'].lower(),
                        'EORINumber': customer['EORINumber'],
                        'UseGLNinElectronicDocument': customer['UseGLNinElectronicDocument'],
                        'ReminderTermsCode': customer['ReminderTermsCode'],
                        'ReminderAmounts': customer['ReminderAmounts'],
                        'ReminderAmountsLCY': customer['ReminderAmountsLCY'],
                        'TaxAreaCode': customer['TaxAreaCode'],
                        'TaxAreaID': customer['TaxAreaID'],
                        'TaxLiable': customer['TaxLiable'],
                        'CurrencyFilter': customer['CurrencyFilter'],
                        'EnterpriseNo': customer['EnterpriseNo']
                    }
                )
            return JsonResponse({'message': "Customers Created!"})

    return JsonResponse({'message': "Customers Created!"})


@api_view(['POST'])
def createUserBC(request):
    # permission_classes = (IsAuthenticated,)
    serializer = CreateUserFromBc(
        data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email'].lower()
    password = serializer.validated_data['password']
    try:
        bc_customer = BCCustomer.objects.filter(EMail=email).last()
        try:
            User.objects.create(
                name=bc_customer.Name,
                email=bc_customer.EMail.lower(),
                addressLine1=bc_customer.Address,
                addressLine2=bc_customer.Address2,
                region_code=bc_customer.County,
                language_code=bc_customer.LanguageCode,
                city=bc_customer.City,
                enterprise_no=bc_customer.EnterpriseNo,
                postalCode=bc_customer.PostCode,
                phoneNumber=bc_customer.PhoneNo,
                mobile_phoneNumber=bc_customer.TelexNo,
                customer_id=bc_customer.No,
                CustomerPriceGroup=bc_customer.CustomerPriceGroup,
                password=password,
                Vat=bc_customer.VATRegistrationNo,
                is_active=True
            )
        except:
            return Response("Customer Already Exists!", status=status.HTTP_404_NOT_FOUND)
        try:
            subject = "User Created!"
            message = f'Customer Registered from {email}.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ['info@exoticcity.be']
            send_mail(subject, message, email_from, recipient_list)
        except:
            return Response("Authentication For SMTP Failed!", status=status.HTTP_404_NOT_FOUND)
    except BCCustomer.DoesNotExist:
        return Response("customer not exist", status=status.HTTP_404_NOT_FOUND)
        # Handle the case where BCCustomer with the given email does not exist
    return Response("User Created!", status=status.HTTP_200_OK)


@api_view(['POST'])
def loginApi(request):
    # permission_classes = (IsAuthenticated,)
    serializer = LoginSerializers(
        data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    password = serializer.validated_data['password']
    authenticate(request, username=user, password=password)
    login(request, user)
    userData= UserSerializer(user)
    return Response(data={"user": userData.data['customer_id']}, status=status.HTTP_200_OK)


@api_view(['POST'])
def otpApi(request):
    otpGenerated = cache.get('otp')
    userCache = cache.get('user')
    serializer = OtpSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    otp = serializer.validated_data.get('otp')
    if int(otp) == otpGenerated:
        login(request, userCache)
        user = UserSerializer(userCache)
        return Response(data={"user": user.data['customer_id']}, status=status.HTTP_200_OK)
    return Response(data={"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)


class UserCreateAPIView(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        subject = "Customer Created!"
        message = f'New Customer Registered From Exotic City Web Portal!.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['info@exoticcity.be']
        send_mail(subject, message, email_from, recipient_list)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GetUserByCustomerIdView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        customer_id = self.kwargs.get('customerId')
        if customer_id:
            return get_object_or_404(User, customer_id=customer_id)
        raise Http404()
        

def updateCustomer(self, custNo):
    try:
        url = f"https://api.businesscentral.dynamics.com/v2.0/Live/api/bctech/demo/v2.0/Companies(f03f6225-081c-ec11-bb77-000d3abcd65f)/customer?$filter = No eq '{custNo}'"
        response = requests.get(url, headers=getToken())
        if Customer.objects.filter(customer_id=custNo).exists():
            customer = Customer.objects.get(customer_id=custNo)
            customer.name = response.json()['value'][0]['Name']
            customer.email = response.json()['value'][0]['EMail'].lower()
            customer.addressLine1 = response.json()['value'][0]['Address']
            customer.addressLine2 = response.json()['value'][0]['Address2']
            customer.region_code = response.json()['value'][0]['CountryRegionCode']
            customer.language_code = response.json()['value'][0]['LanguageCode']
            customer.city = response.json()['value'][0]['City']
            customer.enterprise_no = response.json()['value'][0]['EnterpriseNo']
            customer.CustomerPriceGroup = response.json()['value'][0]['CustomerPriceGroup']
            customer.Vat = response.json()['value'][0]['VATRegistrationNo']
            customer.postalCode = response.json()['value'][0]['PostCode']
            customer.phoneNumber = response.json()['value'][0]['PhoneNo']
            customer.mobile_phoneNumber = response.json()['value'][0]['TelexNo']
            customer.is_active = True
            customer.save()
            return JsonResponse({"success": "Customer Verified"})
        else:
            return JsonResponse({"error": "Customer Not Found"})
    except Exception as e:
        return JsonResponse({"error": f"Customer Not Found or {e}"}) 

from django.db import transaction
from django.db.models import Window, F
from django.db.models.functions import RowNumber

def delete_duplicate_users(self):
    # Begin a transaction
    with transaction.atomic():
        # Annotate each user with a row number, partitioned by email and ordered by 'id'
        users_with_row_number = BCCustomer.objects.annotate(
            row_number=Window(
                expression=RowNumber(),
                partition_by=[F('EMail')],
                order_by=F('id').asc()
            )
        )

        # Use a list comprehension to collect IDs of duplicates (rows with row_number greater than 1)
        duplicate_ids = [user.id for user in users_with_row_number if user.row_number > 1]

        # Delete duplicates using the list of IDs
        BCCustomer.objects.filter(id__in=duplicate_ids).delete()
def deleteUser(self, user_id):
    try:
        if BCCustomer.objects.filter(No=user_id).exists():
            BCCustomer.objects.get(No=user_id).delete()
        if Customer.objects.filter(customer_id=user_id).exists():
            Customer.objects.get(customer_id=user_id).delete()
        return JsonResponse({"success": "Customer Deleted From Web!"}) 
    except Exception as e:
        return JsonResponse({"error": f"{e}"}) 
    
def syncCustomerOnWeb(self, user_id):
    try:
        url = f"https://api.businesscentral.dynamics.com/v2.0/Live/api/bctech/demo/v2.0/Companies(f03f6225-081c-ec11-bb77-000d3abcd65f)/customer?$filter = No eq '{user_id}'"
        response = requests.get(url, headers=getToken())
        if response.status_code == 200:
            data = response.json()
            for customer in data['value']:
                cust, created = BCCustomer.objects.update_or_create(
                    No=customer['No'],
                    EMail= customer['EMail'].lower(),
                    defaults={
                        'Name': customer['Name'],
                        'SearchName': customer['SearchName'],
                        'Name2': customer['Name2'],
                        'Address': customer['Address'],
                        'Address2': customer['Address2'],
                        'City': customer['City'],
                        'Contact': customer['Contact'],
                        'PhoneNo': customer['PhoneNo'],
                        'Blocked': customer['Blocked'],
                        'DocumentSendingProfile': customer['DocumentSendingProfile'],
                        'ShiptoCode': customer['ShiptoCode'],
                        'OurAccountNo': customer['OurAccountNo'],
                        'TerritoryCode': customer['TerritoryCode'],
                        'GlobalDimension1Code': customer['GlobalDimension1Code'],
                        'GlobalDimension2Code': customer['GlobalDimension2Code'],
                        'ChainName': customer['ChainName'],
                        'BudgetedAmount': customer['BudgetedAmount'],
                        'CreditLimitLCY': customer['CreditLimitLCY'],
                        'CustomerPostingGroup': customer['CustomerPostingGroup'],
                        'CurrencyCode': customer['CurrencyCode'],
                        'CustomerPriceGroup': customer['CustomerPriceGroup'],
                        'LanguageCode': customer['LanguageCode'],
                        'RegistrationNumber': customer['RegistrationNumber'],
                        'StatisticsGroup': customer['StatisticsGroup'],
                        'PaymentTermsCode': customer['PaymentTermsCode'],
                        'SalespersonCode': customer['SalespersonCode'],
                        'ShipmentMethodCode': customer['ShipmentMethodCode'],
                        'PlaceofExport': customer['PlaceofExport'],
                        'CustomerDiscGroup': customer['CustomerDiscGroup'],
                        'CountryRegionCode': customer['CountryRegionCode'],
                        'Amount': customer['Amount'],
                        'DebitAmount': customer['DebitAmount'],
                        'CreditAmount': customer['CreditAmount'],
                        'InvoiceAmounts': customer['InvoiceAmounts'],
                        'OtherAmountsLCY': customer['OtherAmountsLCY'],
                        'Comment': customer['Comment'],
                        'LastStatementNo': customer['LastStatementNo'],
                        'Prepayment': customer['Prepayment'],
                        'PartnerType': customer['PartnerType'],
                        'Payments': customer['Payments'],
                        'PostCode': customer['PostCode'],
                        'PrintStatements': customer['PrintStatements'],
                        'PricesIncludingVAT': customer['PricesIncludingVAT'],
                        'ProfitLCY': customer['ProfitLCY'],
                        'BilltoCustomerNo': customer['BilltoCustomerNo'],
                        'Priority': customer['Priority'],
                        'PaymentMethodCode': customer['PaymentMethodCode'],
                        'LastModifiedDateTime': customer['LastModifiedDateTime'],
                        'GlobalDimension1Filter': customer['GlobalDimension1Filter'],
                        'GlobalDimension2Filter': customer['GlobalDimension2Filter'],
                        'Balance': customer['Balance'],
                        'BalanceLCY': customer['BalanceLCY'],
                        'BalanceDue': customer['BalanceDue'],
                        'NetChange': customer['NetChange'],
                        'NetChangeLCY': customer['NetChangeLCY'],
                        'SalesLCY': customer['SalesLCY'],
                        'InvAmountsLCY': customer['InvAmountsLCY'],
                        'InvDiscountsLCY': customer['InvDiscountsLCY'],
                        'NoofInvoices': customer['NoofInvoices'],
                        'InvoiceDiscCode': customer['InvoiceDiscCode'],
                        'InvoiceCopies': customer['InvoiceCopies'],
                        'PmtDiscountsLCY': customer['PmtDiscountsLCY'],
                        'PmtToleranceLCY': customer['PmtToleranceLCY'],
                        'BalanceDueLCY': customer['BalanceDueLCY'],
                        'PaymentsLCY': customer['PaymentsLCY'],
                        'CrMemoAmounts': customer['CrMemoAmounts'],
                        'CrMemoAmountsLCY': customer['CrMemoAmountsLCY'],
                        'FinanceChargeMemoAmounts': customer['FinanceChargeMemoAmounts'],
                        'ShippedNotInvoiced': customer['ShippedNotInvoiced'],
                        'ShippedNotInvoicedLCY': customer['ShippedNotInvoicedLCY'],
                        'ShippingAgentCode': customer['ShippingAgentCode'],
                        'ApplicationMethod': customer['ApplicationMethod'],
                        'LocationCode': customer['LocationCode'],
                        'FaxNo': customer['FaxNo'],
                        'VATBusPostingGroup': customer['VATBusPostingGroup'],
                        'VATRegistrationNo': customer['VATRegistrationNo'],
                        'CombineShipments': customer['CombineShipments'],
                        'GenBusPostingGroup': customer['GenBusPostingGroup'],
                        'GLN': customer['GLN'],
                        'County': customer['County'],
                        'EORINumber': customer['EORINumber'],
                        'UseGLNinElectronicDocument': customer['UseGLNinElectronicDocument'],
                        'ReminderTermsCode': customer['ReminderTermsCode'],
                        'ReminderAmounts': customer['ReminderAmounts'],
                        'ReminderAmountsLCY': customer['ReminderAmountsLCY'],
                        'TaxAreaCode': customer['TaxAreaCode'],
                        'TaxAreaID': customer['TaxAreaID'],
                        'TaxLiable': customer['TaxLiable'],
                        'CurrencyFilter': customer['CurrencyFilter'],
                        'EnterpriseNo': customer['EnterpriseNo']
                    }
                )
            return JsonResponse({'message': "Customers Created!"})
    except Exception as e:
        return JsonResponse({'message': f"{e}"})

@api_view(['POST'])
def bcEmailValidation(request):
    email = request.data.get('email').lower()
    if BCCustomer.objects.filter(EMail=email).exists() or Customer.objects.filter(email=email).exists():
        return Response(data="Customer Already Exists in Bussiness Central!", status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(data="OK!", status=status.HTTP_200_OK)



@api_view(['GET'])
def inactiveUserFromWeb(self, customerNo):
    try:
        cust = Customer.objects.get(customer_id=customerNo)
        cust.is_active= False
        cust.save()
        return Response('Customer Blocked From Web Store!', status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(f'Customer Not Found! {e}', status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def changeEmailFromWeb(self, customerNo, email):
    try:
        cust = Customer.objects.get(customer_id=customerNo)
        cust.email= email
        cust.save()
        return Response('Email Changed From Web Store!', status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(f'Customer Not Found! {e}', status=status.HTTP_404_NOT_FOUND)
