from django import setup
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import query
from django.http import HttpResponse # Add this
from django.shortcuts import get_object_or_404

from django.db.models.fields import PositiveIntegerRelDbTypeMixin
from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import View, ListView, DetailView
import json
from django.shortcuts import redirect
from django.contrib import messages
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder, cuponOrder
from .forms import CouponForm, RefundForm, ContactForm, ProfileForm

from django.core.mail import send_mail
from django.template.loader import render_to_string

# EMAIL CONFIRMATION
"""
def order_confirmation(request):
	data = cartData(request)

	order = data['order']
	items = data['items']

	context = {
		'order':order,
		'items':items
	}

	return render(request, 'emails/order_confirmation.html', context)
"""

#--------
#        |
# STORE  |
#        | 
#--------

def create_user(request):
	if request.method == 'POST':
		profile_form = ProfileForm(request.POST, instance=request.user.customer)
		if profile_form.is_valid():
			profile_form.save()
			messages.success(request, ('New user created successfully'))
			return redirect('/')
		else:
			messages.error(request, ('Please correct the error below.'))
	else:
		profile_form = ProfileForm()


	return render(request, 'account/signup_update.html', {
		'profile_form': profile_form
	})


def profile_view(request):
	data = cartData(request)

	order = data['order']
	items = data['items']

	context = {
		'order':order,
		'items':items
	}

	return render(request, 'account/profile.html', context)


def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)


def storeList(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store_list.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	if request.user.is_authenticated:
		if order.get_cart_items == 0:
			order.coupon = None
			request.session['code'] = None
			order.save()
		if order.coupon != None:
			num = order.coupon
			num_value = request.session.get('code_value')
			order.save()
		else:
			num = request.session.get('code')
			num_value = request.session.get('code_value')

	else:
		num = request.session.get('code')
		num_value = request.session.get('code_value')

	if num != None:
		if not request.user.is_authenticated:
			data['order']['get_cart_total'] -= num_value	

	context = {
		'items':items, 
		'order':order,
		'coupon':num,
		'ammount':num_value,
		'cartItems':cartItems,
		'couponform':CouponForm()
	}

	return render(request, 'store/cart.html', context)


def checkout(request):
	data = cartData(request)

	num = request.session.get('code')
	num_value = request.session.get('code_value')

	print(num)
	print(num_value)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	if num != None:
		if not request.user.is_authenticated:
			data['order']['get_cart_total'] -= num_value


	context = {
		'items':items, 
		'order':order,
		'coupon':num,
		'ammount':num_value,
		'cartItems':cartItems,
		'couponform':CouponForm()
	}

	return render(request, 'store/checkout.html', context)


def contact_us(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			sender_name = form.cleaned_data['meno']
			sender_email = form.cleaned_data['email']
			message = "{0} has sent you a new message:\n\n{1}".format(sender_name, form.cleaned_data['Správa'])
			send_mail('New Enquiry', message, sender_email, ['noreply@saulgadgets.com'])
			return HttpResponse('Thanks for contacting us!')
	
	else:
		form = ContactForm()
	
	return render(request, 'store/contact_us.html', {'form': form})


class RequestRefundView(View):

	def get(self, *args, **kwargs):
		form = RefundForm()
		context = {
			'form': form
		}
		return render(self.request, "store/request_refund.html", context)

	def post(self, *args, **kwargs):
		form = RefundForm(self.request.POST)
		if form.is_valid():
			ref_code = form.cleaned_data.get('ref_code')
			message = form.cleaned_data.get('message')
			email = form.cleaned_data.get('email')

			try:
				order = Order.objects.get(temporary_id=ref_code)
				order.refund_requested = True
				order.save()

				refund = Refund()
				refund.order = order
				refund.reason = message
				refund.email = email
				refund.save()

				messages.info(self.request, "Your request was received")

				return redirect("/request_refund")

			except ObjectDoesNotExist:
				messages.info(self.request, "This order does not exist.")
				return redirect("/request_refund")

#---------
#         |
# ITEM	  |
#         | 
#---------

def incident_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "store/incident.html", locals())
			

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
	elif action == 'delete':
		orderItem.quantity = 0

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

#---------
#         |
# ORDER	  |
#         | 
#---------


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

	print(total)
	print(order.get_cart_total)

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
		type_of_delivery=data['shipping']['type_of_delivery'],
		)
	
	if order.coupon:
		obj_coupon = order.coupon
		obj = Coupon.objects.get(code=obj_coupon)
		obj.used_num += 1
		obj.save()

	num = request.session.get('code')
	num_value = request.session.get('code_value')
	if num_value and num is not None:
		num_value = None
		num = None
		request.session['code_value'] = None
		request.session['code'] = None
	else:
		pass
	
	items = order.orderitem_set.all()

	html = render_to_string('emails/order_confirmation.html', {'items': items, 'order':order,})
	send_mail('Order confirmation', 'Your order has been sent!!', 'noreply@saulgadgets.com', ['noreply@saulgadgets.com','mail@saulgadgets.com', customer.email], fail_silently=False, html_message=html)

	return JsonResponse('Payment submitted..', safe=False)

#---------
#         |
# COUPON  |
#         | 
#---------


def get_coupon(request, code):
	try:
		coupon = Coupon.objects.get(code=code)
		return coupon
	except ObjectDoesNotExist:
		messages.info(request, "This coupon does not exist")
		return render(request, 'store/cart.html')

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

					order.coupon = Coupon.objects.get(code=code)
					order.save()

					if order.get_cart_items == 0:
						order.coupon = None
						order.save()
					if order.coupon != None:
						num = order.coupon
						num_value = request.session.get('code_value')
						order.save()
					else:
						num = request.session.get('code')
						num_value = request.session.get('code_value')
						num_value = None
						num = None

					context = {
						'items':items,
						'coupon': num,
						'ammount':num_value,
						'order':order, 
						'cartItems':cartItems,
						'couponform':CouponForm()
					}

					messages.success(request, "Coupon activated")
					return render(request, 'store/cart.html', context)

				else:
					order = cuponOrder(request, data, code)
					
					cartItems = data['cartItems']
					order = data['order']
					items = data['items']
					
					obj = Coupon.objects.get(code=code)
					field_object = Coupon._meta.get_field("ammount")
					field_value = field_object.value_from_object(obj)

					data['order']['get_cart_total'] -= field_value

					if order['get_cart_total'] < 0:
						code = None
						field_value = None
						order['get_cart_total'] = 0

					context = {
						'items':items,
						'coupon': code,
						'ammount':field_value, 
						'order':order, 
						'cartItems':cartItems,
						'couponform':CouponForm()
					}

					messages.success(request, "Coupon activated")
					return render(request, 'store/cart.html', context)

			except ObjectDoesNotExist:
				messages.info(request, "Coupon does not exists ")
				num = request.session.get('code')
				num_value = request.session.get('code_value')

				cartItems = data['cartItems']
				items = data['items']
				
				if not request.user.is_authenticated:
					temporary_id = data['order']['temporary_id']
					instance = Order.objects.filter(temporary_id=temporary_id)
					instance.delete()
				
				order = data['order']
				
				if num_value is not None:
					num_value = None
				request.session['code_value'] = None

				if num is not None:
					num = None
				request.session['code'] = None

				if request.user.is_authenticated:
					if order.coupon != None:
						num = order.coupon
						num_value = order.coupon.ammount
						order.save()

				context = {
					'items':items, 
					'order':order,
					'coupon': num,
					'ammount':num_value, 
					'cartItems':cartItems,
					'couponform':CouponForm()
				}

				return render(request, 'store/cart.html', context)
	
	return None


