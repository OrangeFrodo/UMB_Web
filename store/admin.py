from django.contrib import admin

from .models import *

def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)
    make_refund_accepted.short_description = 'Update orders to refund granted'

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'customer', 
                    'complete', 
                    'being_delivered', 
                    'recived', 
                    'refund_requested', 
                    'refund_granted',
                    'coupon',
                ]

    list_display_links = [ 'customer',
                            'complete',
                            'coupon',
                ]

    list_filter = [ 'complete', 
                    'being_delivered', 
                    'recived', 
                    'refund_requested', 
                    'refund_granted',
                ]
    
    search_fields = [
        'customer__last_name',
        'temporary_id'
    ]

    actions = [make_refund_accepted]

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Coupon)