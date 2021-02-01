from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import JsonResponse
import json
from django.shortcuts import redirect
from django.contrib import messages
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder, cuponOrder
from .forms import CouponForm

def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)


def cart(request):
	data = cartData(request)

	if request.user.is_authenticated:
		num = request.session.get('code')
		num_value = request.session.get('code_value')

	else:
		num = None
		num_value = None
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {
		'items':items, 
		'order':order,
		'coupon':num,
		'ammount':num_value,
		'cartItems':cartItems,
	}

	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	if request.user.is_authenticated:
		try:
			num = order.coupon.code
			num_value = request.session.get('code_value')
		except:
			num = request.session.get('code')
			num_value = request.session.get('code_value')
	else:
		num = None
		num_value = None

	context = {
		'items':items, 
		'order':order,
		'coupon':num,
		'ammount':num_value,
		'cartItems':cartItems,
		'couponform':CouponForm()
	}

	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	num = request.session.get('code')
	num_value = request.session.get('code_value')
	if num_value and num is not None:
		num_value = None
		num = None
		request.session['code_value'] = None
		request.session['code'] = None
	else:
		pass

	return JsonResponse('Payment submitted..', safe=False)

def get_coupon(request, code):
	try:
		coupon = Coupon.objects.get(code=code)
		return coupon
	except ObjectDoesNotExist:
		messages.info(request, "This coupon does not exist")
		return render(request, 'store/checkout.html')

def add_coupon(request):
	data = cartData(request)
	if request.method == "POST":
		form = CouponForm(request.POST or None)
		if form.is_valid():
			code = form.cleaned_data.get('code')
			try:
				num = request.session.get('code')
				num_value = request.session.get('code_value')

				if num is None:
					num = code
				request.session['code'] = code

				obj = Coupon.objects.get(code=code)
				field_object = Coupon._meta.get_field("ammount")
				field_value = field_object.value_from_object(obj)

				if num_value is None:
					num_value = field_value
				request.session['code_value'] = field_value

				if request.user.is_authenticated:
					customer = request.user.customer
					order, created = Order.objects.get_or_create(customer=customer, complete=False)

					cartItems = data['cartItems']
					order = data['order']
					items = data['items']

					context = {
						'items':items,
						'coupon': code,
						'ammount':field_value,
						'order':order, 
						'cartItems':cartItems,
						'couponform':CouponForm()
					}

					order.coupon = Coupon.objects.get(code=code)
					order.save()
					messages.success(request, "Coupon activated")
					return render(request, 'store/checkout.html', context)

				else:
					order = cuponOrder(request, data, code)

					cartItems = data['cartItems']
					order = data['order']
					items = data['items']
					
					obj = Coupon.objects.get(code=code)
					field_object = Coupon._meta.get_field("ammount")
					field_value = field_object.value_from_object(obj)

					order['get_cart_total'] -= field_value

					context = {
						'items':items,
						'coupon': code,
						'ammount':field_value, 
						'order':order, 
						'cartItems':cartItems,
						'couponform':CouponForm()
					}

					messages.success(request, "Coupon activated")
					return render(request, 'store/checkout.html', context)

			except ObjectDoesNotExist:
				messages.info(request, "Coupon does not exists ")
				if request.user.is_authenticated:
					num_value = request.session.get('code_value')

					cartItems = data['cartItems']
					order = data['order']
					items = data['items']
					
					num = order.coupon.code

					context = {
						'items':items, 
						'order':order,
						'coupon': num,
						'ammount':num_value,
						'cartItems':cartItems,
						'couponform':CouponForm()
					}

				else:
					cartItems = data['cartItems']
					order = data['order']
					items = data['items']

					context = {
						'items':items, 
						'order':order,
						'cartItems':cartItems,
						'couponform':CouponForm()
					}

				return render(request, 'store/checkout.html', context)
	
	return None

	
