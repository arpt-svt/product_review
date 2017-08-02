from django.db.models import Avg
from decimal import Decimal
from rest_framework.serializers import (
	ModelSerializer,
	ValidationError,
	SerializerMethodField,
	DateTimeField,
	StringRelatedField,
	HyperlinkedIdentityField,
	)

from product_review.models import (
	Product,
	Sale,
	Rating,
	)


class ProductSerializer(ModelSerializer):
	rating = SerializerMethodField()
	finalPrice = SerializerMethodField()
	inStock = SerializerMethodField()
	productDetail = HyperlinkedIdentityField(view_name='product_review_api:detail_product',lookup_field='id')

	def get_rating(self,obj):
		product = obj.id
		rating = Rating.objects.filter(product=product).aggregate(Avg('rate'))
		rating = rating.get('rate__avg')
		if rating:
			# Choping of decimals after one place from rating
			rating *= 10
			rating = int(rating)
			rating = rating/10.0
			return rating
		else:
			return 'NO ratings'

	def get_finalPrice(self,obj):
		return obj.getPrice()

	def get_inStock(self,obj):
		return obj.getInStock()

	def validate(self,data):
		price = data.get('price')
		quantity = data.get('quantity')
		discountPercent = data.get('discountPercent' or None)
		errors = {}
		if price<1:
			errors['price'] = ['Price must be greate than 0']
		if quantity<1:
			errors['quantity'] = ['Quantity must be greate than 0']
		if discountPercent:
			if discountPercent<1:
				errors['discountPercent'] = ['Discout percent must be greate than 0 or blank']
		if errors:
			raise ValidationError(errors)
		return data
	class Meta:
		model = Product
		fields = ['productDetail','id','name','picture','price','quantity','discountPercent','finalPrice','rating','inStock']

class ProdductDetailHelperRatingSerializer(ModelSerializer):
	user = StringRelatedField()
	class Meta:
		model = Rating
		fields = ['user','rate']

class ProductDetailSerializer(ModelSerializer):
	rating = SerializerMethodField()
	finalPrice = SerializerMethodField()
	inStock = SerializerMethodField()
	rating_set = ProdductDetailHelperRatingSerializer(many=True)
	def get_rating(self,obj):
		product = obj.id
		rating = Rating.objects.filter(product=product).aggregate(Avg('rate'))
		rating = rating.get('rate__avg')
		if rating:
			# Choping of decimals after one place from rating
			rating *= 10
			rating = int(rating)
			rating = rating/10.0
			return rating
		else:
			return 'NO ratings'

	def get_finalPrice(self,obj):
		return obj.getPrice()

	def get_inStock(self,obj):
		return obj.getInStock()

	class Meta:
		model = Product
		fields = ['id','name','picture','price','quantity','discountPercent','finalPrice','rating_set','inStock','rating']	

class SaleSerializer(ModelSerializer):
	createdAt = DateTimeField(read_only=True)

	def validate_product(self,product):
		if product:
			if product.active:
				return product
			else:
				raise ValidationError('The product is not available')
		else:
			raise ValidationError('Please select a valid product')
	
	def validate(self,data):
		quantityOrdered = data.get('quantity')
		product = data.get('product')
		quantity = product.quantity
		if quantityOrdered < 1:
			raise ValidationError({'quantity':['Quantity must be greater than or equals to 1']})
		if quantity < quantityOrdered:
			if quantity == 0:
				msz = 'This product is out of stock'
			else:
				msz = 'Sorry we have only %d left in stock'%(quantity)
			raise ValidationError(msz)
		return data

	def create(self,validatedData):
		product = validatedData.get('product')
		quantity = validatedData.get('quantity')
		user = self.context['request'].user
		totalPrice  = Decimal(product.getPrice())*quantity
		print (totalPrice)
		product.quantity = product.quantity - quantity
		product.save()
		saleObj = Sale.objects.create(product=product,user=user,quantity=quantity,price=totalPrice)
		return saleObj

	class Meta:
		model = Sale
		fields = ['product','quantity','price','createdAt']

		extra_kwargs = {'price': {'read_only': True}}

class RatingSerializer(ModelSerializer):
	def validate_product(self,product):
		if not product.active:
			raise ValidationError('This product does not exists')
		return product

	def validate_rate(self,rate):
		if rate<1:
			raise ValidationError('Rating must be between[1-5]')
		return rate
	class Meta:
		model = Rating
		fields = ['product','rate']

# {
# 	"product":1,
# 	"user":1,
# 	"rate":11
# }