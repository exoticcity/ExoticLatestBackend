from django.db import models
import uuid
import datetime
from customer.models import *


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ItemNo = models.CharField(max_length=200, blank=True, null=True, unique=True)
    Description = models.CharField(max_length=255, blank=True, null=True)
    Blocked = models.BooleanField(default=False, blank=True, null=True)
    SearchDescription = models.CharField(max_length=255, blank=True, null=True)
    BaseUnitOfMeasure = models.CharField(max_length=500, blank=True, null=True)
    ParentCategory = models.CharField(max_length=500, blank=True, null=True)
    ItemCategoryCode = models.CharField(max_length=500, blank=True, null=True)
    ItemSubCategoryCode = models.CharField(
        max_length=500, blank=True, null=True)
    Brand = models.CharField(max_length=500, blank=True, null=True)
    NetWeight = models.FloatField(blank=True, null=True)
    Packaging = models.CharField(max_length=500, blank=True, null=True)
    BarCode = models.CharField(max_length=200, blank=True, null=True)
    SalesUnitOfMeasure = models.CharField(max_length=500, blank=True, null=True)
    WeightDescription = models.CharField(max_length=100, blank=True, null=True)
    Type = models.CharField(max_length=500, blank=True, null=True)
    vat = models.IntegerField(blank=True, null=True)
    Quantity = models.IntegerField(default=0, blank=True, null=True)
    BrandLink = models.CharField(max_length=255, blank=True, null=True)
    GTIN = models.CharField(max_length=200, blank=True, null=True)
    PurchasingCode = models.CharField(max_length=500, blank=True, null=True)
    LastDateTimeModified = models.DateTimeField(default=datetime.datetime.now())
    # Picture = models.CharField(max_length=500, blank=True, null=True)
    SalesBlocked = models.BooleanField(default=False, blank=True, null=True)
    Picture = models.ImageField(upload_to='images/', blank=True, null=True)  # Updated to ImageField

    def __str__(self):
        return f"Product {self.ItemNo}: {self.Description}"

class SalesPrice(models.Model):
    Srno = models.CharField(max_length=100, unique=True, blank=True, null=True)
    salestype = models.CharField(max_length=100, blank=True, null=True)
    Salecode = models.CharField(max_length=10, blank=True, null=True)
    ItemNo = models.CharField(max_length=50, blank=True, null=True)
    UnitPrice = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    MinimumQuantity = models.IntegerField(blank=True, null=True)
    StartDate = models.DateField(blank=True, null=True)
    EndDate = models.DateField(blank=True, null=True)
    SystemModifiedAt = models.CharField(max_length=200,blank=True, null=True)

    def __str__(self):
        return f"Product {self.ItemNo}"


class LastTimeUpdation(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    timeStamp = models.DateTimeField()

class Cart(models.Model):
    cart_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    total_amount_including_vat = models.FloatField(blank=True, null=True)
    total_amount_excluding_vat = models.FloatField(blank=True, null=True)
    vat_amount = models.FloatField(blank=True, null=True)
    date_time_created = models.DateTimeField(default=datetime.datetime.today(), blank=True, null=True)

    def __str__(self):
        return self.customer.email

class CartItem(models.Model):
    cart_item_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    vat_rate = models.FloatField(default=0, blank=True, null=True)
    total_amount_including_vat = models.FloatField(default=0, blank=True, null=True)
    total_amount_excluding_vat = models.FloatField(default=0, blank=True, null=True)
    vat_amount = models.FloatField(default=0, blank=True, null=True)
    date_time_created = models.DateTimeField(default=datetime.datetime.today(), blank=True, null=True)

    def __str__(self):
        return self.product.ItemNo

    class Meta:
        unique_together= ('cart', 'product')
