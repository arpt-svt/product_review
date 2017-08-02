from django.http import Http404

from django.shortcuts import get_object_or_404
from rest_framework.generics import (
	CreateAPIView,
	ListAPIView,
	RetrieveAPIView,
	)
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from product_review.models import (
	Product,
	Sale,
	Rating,
	)
from .serializer import (
	ProductSerializer,
	SaleSerializer,
	RatingSerializer,
	ProductDetailSerializer,
	)


class ProductCreateAPIView(CreateAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	permission_classes = (IsAdminUser,)

class ProductListAPIView(ListAPIView):
	queryset = Product.objects.filter(active=True)
	serializer_class = ProductSerializer

class ProductDetailAPIView(RetrieveAPIView):
	queryset = Product.objects.filter(active=True)
	serializer_class = ProductDetailSerializer
	lookup_field = 'id'

class SaleCreateAPIView(CreateAPIView):
	queryset = Sale.objects.all()
	serializer_class = SaleSerializer

class UserPurchaseListAPIView(ListAPIView):
	serializer_class = SaleSerializer
	def get_queryset(self):
		user = self.request.user
		return user.sale_set.all()

class RatingAPIView(APIView):
	def post(self,request):
		serializer = RatingSerializer(data=request.data)
		if serializer.is_valid():
			data = serializer.validated_data
			product = data.get('product') 
			rate = data.get('rate')
			user = request.user
			#checking if the user bought this product
			saleQs = Sale.objects.filter(user=user,product=product)
			if not saleQs.exists():
				context = {'error':'You did not have permission to rate this product'}
				return Response(context, status=status.HTTP_400_BAD_REQUEST)
			# checking if the user already rated for the product
			ratingQs = Rating.objects.filter(user=user,product=product)
			if ratingQs.exists():
				#already rated 
				rating = ratingQs.first()
				serializer = RatingSerializer(rating,data=request.data)
				if serializer.is_valid():
					serializer.save()
			else:
				#Rating first time
				serializer.save(user=user)
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteProductAPIView(APIView):
	permission_classes = (IsAdminUser,)
	def delete(self, request, id):
		product = get_object_or_404(Product,id=id)
		if not product.active:
			return Response(status=status.HTTP_404_NOT_FOUND)
		product.active = False
		# on deletion setting quantity to 0
		product.quantity = 0
		product.save()
		return Response(status=status.HTTP_204_NO_CONTENT)