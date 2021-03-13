import json
import uuid
from .models import *

def cookieCart(request):
	#Create empty cart for now for non-logged in user
	try:
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart = {'temporary_id' : uuid.uuid4()}
		print('CART:', cart)

	temporary_id = cart['temporary_id']

	items = []
	order = {'get_cart_total':0, 'get_cart_items':0, 'temporary_id': temporary_id, 'shipping':False}
	cartItems = order['get_cart_items']

	for i in cart:

		try:	
				if(cart[i]['quantity']>0): #items with negative quantity = lot of freebies  
					cartItems += cart[i]['quantity']

					product = Product.objects.get(id=i)
					total = (product.price * cart[i]['quantity'])

					order['get_cart_total'] += total
					order['get_cart_items'] += cart[i]['quantity']

					item = {
						'id':product.id,
						'product':{'id':product.id,'name':product.name, 'price':product.price, 
						'imageURL':product.imageURL}, 'quantity':cart[i]['quantity'],
						'digital':product.digital,'get_total':total,
						}
					items.append(item)

					if product.digital == False:
						order['shipping'] = True
		except:
			pass
			
	return {'cartItems':cartItems ,'order':order, 'items':items}

def cartData(request):
	if request.user.is_authenticated:
		cookieData = cookieCart(request)
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, temporary_id=cookieData['order']['temporary_id'], complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		cookieData = cookieCart(request)
		cartItems = cookieData['cartItems']
		order = cookieData['order']
		items = cookieData['items']

	return {'cartItems':cartItems ,'order':order, 'items':items}

	
def guestOrder(request, data):
	first_name = data['form']['first_name']
	name = data['form']['name']
	email = data['form']['email']
	phone = data['form']['phone']

	cookieData = cookieCart(request)
	temporary_id = cookieData['order']['temporary_id']
	items = cookieData['items']

	customer, created = Customer.objects.get_or_create(
			email=email,
			phone=phone,
			)
	customer.name = name
	customer.first_name = first_name
	customer.save()

	order, created = Order.objects.get_or_create(
		temporary_id=temporary_id,
		complete=False,
	)

	order.customer = customer
	order.save()

	for item in items:
		product = Product.objects.get(id=item['id'])
		orderItem = OrderItem.objects.create(
			product=product,
			order=order,
			quantity=(item['quantity'] if item['quantity']>0 else -1*item['quantity']),
		)
		
	return customer, order


def cuponOrder(request, data, code):
	cookieData = cookieCart(request)

	temporary_id = data['order']['temporary_id']
	items = cookieData['items']

	order, created = Order.objects.update_or_create(
		temporary_id = temporary_id,
		complete=False,
		defaults={'coupon': Coupon.objects.get(code=code)}
		)

	order.save()

	return order