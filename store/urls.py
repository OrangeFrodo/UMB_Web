from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('add-coupon/', views.add_coupon, name='add-coupon'),
	path('order_confirmation/', views.order_confirmation, name='order_confirm'),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
	path('request_refund/', views.RequestRefundView.as_view(), name="request_refund")

]