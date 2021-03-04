from allauth.account.models import EmailAddress
from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.db.models.fields import CharField, NullBooleanField
from django.db.models.signals import post_save
from django.utils.html import mark_safe
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

#_______
#			|
# CUSTOMER 	|
#			|
#_______	|

class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	first_name = models.CharField('krstné_meno', max_length=50, null=True, blank=True)
	last_name = models.CharField('priezvisko', max_length=50, null=True, blank=True)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)
	phone = PhoneNumberField(null=False, blank=True)

	def create_customer_profile(sender, instance, created, **kwargs):
		if created:
			Customer.objects.create(user=instance, 
									name=instance.username, 
									email=instance.email, 
									first_name= instance.first_name,
									last_name=instance.last_name,
									)

			EmailAddress.objects.create(user=instance,
										email=instance.email)

	post_save.connect(create_customer_profile, sender=User)

	def __str__(self):
		return self.name

#_______
#			|
# PRODUCT 	|
#			|
#_______	|

class Product(models.Model):

	VARIANTS = (
		('None', 'None'),
		('Size', 'Size'),
		('Color', 'Color'),
		('Size-Color', 'Size-Color'),
	)

	name = models.CharField(max_length=200)
	price = models.FloatField()
	digital = models.BooleanField(default=False,null=True, blank=True)
	
	image = models.ImageField(null=True, blank=True)
	slug = models.SlugField()

	variant = models.CharField(max_length=10, choices=VARIANTS, default='None')

	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url
	

	def get_absolute_url(self):
		return reverse("store:product", kwargs={
			'slug': self.slug
		})

class Color (models.Model):
	name = models.CharField(max_length=20)
	code = models.CharField(max_length=10, blank=True, null=True)

	def __str__(self):
		return self.name
	
	def color_tag(self):
		if self.code is not None:
			return mark_safe('<p style="background-color:{}">Color </p>'.format(self.code))
		else:
			return ""


class Size(models.Model):
	name = models.CharField(max_length=20)
	code = models.CharField(max_length=10, blank=True, null=True)

	def __str__(self):
		return self.name


class Variants(models.Model):
	title = models.CharField(max_length=100, blank=True, null=True)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
	size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
	price = models.FloatField(default=0)

	def __str__(self):
		return self.title


#_______
#		|
# ORDER |
#		|
#_______|


class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)
	temporary_id = models.CharField(max_length=100, null=True)
	
	coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)

	being_delivered = models.BooleanField(default=False)
	shipped_date = models.DateTimeField(blank=True, null=True)

	recived = models.BooleanField(default=False)
	refund_requested = models.BooleanField(default=False)
	refund_granted = models.BooleanField(default=False)


	def __str__(self):
		return str(self.id)
		
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		if self.coupon:
			total -= self.coupon.ammount
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	type_of_delivery = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address


class Coupon(models.Model):
	code = models.CharField(max_length=15)
	ammount = models.FloatField()
	used_num = models.IntegerField(blank=True, null=True)

	def __str__(self):
		return self.code

class Refund(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	reason = models.TextField()
	accepted = models.BooleanField(default=False)
	email = models.EmailField()

	def __str__(self):
		return f"{self.pk}"
