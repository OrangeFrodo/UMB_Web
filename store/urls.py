from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path("detail/<str:product_id>/", views.incident_view, name="incident"),

	#path('detail/<id>/<slug>/',views.ProductDetailView.as_view(), name="detail"),

	#path('store_list', views.storeList, name="store_list"),

	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('add-coupon/', views.add_coupon, name='add-coupon'),
	
	#path('order_confirmation/', views.order_confirmation, name='order_confirm'),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),

	path('request_refund/', views.RequestRefundView.as_view(), name="request_refund"),
	path('contact_us/', views.contact_us, name='contact_us'),
	path('profile/', views.profile_view, name='profile'),
	path('create_user/', views.create_user, name='create_user')
]