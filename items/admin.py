from django.contrib import admin
from items.models import *

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    search_fields = ['ItemNo', 'Description',
                     'Blocked', 'SearchDescription' ]
    list_display = ['ItemNo', 'Description',
                    'Blocked', 'SearchDescription' ]
    list_filter = ['ItemNo', 'Description',
                   'Blocked', 'SearchDescription' ]
    list_per_page = 20  # Apply pagination
from django.contrib import admin
from items.models import *

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    search_fields = ['ItemNo', 'Description',
                     'Blocked', 'SearchDescription' ]
    list_display = ['ItemNo', 'Description',
                    'Blocked', 'SearchDescription' ]
    list_filter = ['ItemNo', 'Description',
                   'Blocked', 'SearchDescription' ]
    list_per_page = 20  # Apply pagination


class SalesPriceAdmin(admin.ModelAdmin):
    search_fields = ['ItemNo']
    list_display = ['ItemNo', 'Salecode']
    list_filter = ['ItemNo', 'Salecode']
    list_per_page = 20  # Apply pagination


admin.site.register(Product, ProductAdmin)
admin.site.register(SalesPrice, SalesPriceAdmin)
admin.site.register(LastTimeUpdation)
admin.site.register(Cart)
admin.site.register(CartItem)
