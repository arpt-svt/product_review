from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models
# Create your models here.

User = get_user_model()


class Product(models.Model):
	name = models.CharField(max_length=500)
	picture = models.ImageField(upload_to='products/',default='products/None/default.png',height_field=None,width_field=None)
	# Values from 0 to 2147483647
	quantity = models.PositiveIntegerField()
	price = models.DecimalField(max_digits=8, decimal_places=2)
	# ASSUMING MAXIMUM DISCOUNT THAT CAN BE OFFERED IS 99.99 %
	discountPercent = models.DecimalField(max_digits=4, decimal_places=2,blank=True,null=True)
	active = models.BooleanField(default=True)

	def __str__(self):
		return self.name

	def getPrice(self):
		discount = self.discountPercent
		price = self.price
		if discount:
			finalPrice = ((100 - discount)*price)/100
			return format(round(finalPrice,2), '.2f')
		else:
			return str(price)

	def getInStock(self):
		quantity = self.quantity
		if quantity > 0:
			return True
		else:
			return False


class Sale(models.Model):
	product = models.ForeignKey(
		Product,on_delete=models.SET_NULL, 
		null=True,
		)
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		)
	# Values from 0 to 32767
	quantity = models.PositiveSmallIntegerField()
	#The price at which user bought the product
	price = models.DecimalField(max_digits=8, decimal_places=2)
	#To display name even if the product is deleted from db
	#name = models.CharField(max_length=500)
	createdAt = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.username


class Rating(models.Model):
	product = models.ForeignKey(
		Product,
		on_delete=models.CASCADE,
		)
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		)
	rate = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)])

	def __str__(self):
		return self.product.name + " - " + self.user.username

# username = arpit
# pass = mistay@123

# Admin 
# username = mistay
# pass = mistay@123