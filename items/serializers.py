from rest_framework import serializers
from .models import *
import datetime

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesPrice
        fields = ['ItemNo','L1', 'L2', 'L3', 'L4', 'L5', 'promotion']
    def to_representation(self, instance):
        data = super().to_representation(instance)
        today = datetime.date.today()
        if instance.startDate <= today <= instance.endDate:
            data['promotion'] = instance.promotion
            data.pop('L1', None)
            data.pop('L2', None)
            data.pop('L3', None)
            data.pop('L4', None)
            data.pop('L5', None)
        else:
            data.pop('promotion', None)
        return data

class CartItemsSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

    def to_representation(self, instance):
        products = []
        data = super(CartSerializer, self).to_representation(instance)
        products.append(CartItemsSerializer(instance.cart.filter(quantity__gt=0), many=True).data)
        data['items_in_cart'] = products
        return data