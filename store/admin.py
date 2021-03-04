from django.contrib import admin
import datetime
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import *

def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)
    make_refund_accepted.short_description = 'Update orders to refund granted'

def admin_order_being_delivered(modeladmin, request, queryset):
    queryset.update(shipped_date = datetime.datetime.now())
    queryset.update(being_delivered=True)
    
    for order in queryset:
        order.save()
        items = order.orderitem_set.all()
        html = render_to_string('emails/order_sent.html', {'items': items, 'order':order,})
        send_mail('Order confirmation', 'Your order has been sent!!', 'noreply@saulgadgets.com', ['noreply@saulgadgets.com','mail@saulgadgets.com', order.customer.email], fail_silently=False, html_message=html)

admin_order_being_delivered.short_description = 'Shipped order'

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order',
                    'product',
                    'quantity'
                ]

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

    actions = [make_refund_accepted, admin_order_being_delivered]

class ProductVariantsInLine(admin.TabularInline):
    model = Variants
    extra = 1
    show_change_link = True

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'digital']
    inlines = [ProductVariantsInLine]

class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'color_tag']

class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']

class VariantsAdmin(admin.ModelAdmin): 
    list_display = ['title', 'product', 'color', 'size']

admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAddress)
admin.site.register(Coupon)

admin.site.register(Color, ColorAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Variants, VariantsAdmin)