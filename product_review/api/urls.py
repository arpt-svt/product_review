from django.conf.urls import url

from .views import (
	ProductCreateAPIView,
	ProductListAPIView,
	SaleCreateAPIView,
	UserPurchaseListAPIView,
	RatingAPIView,
	DeleteProductAPIView,
	ProductDetailAPIView,
	)

urlpatterns = [
    url(r'^add/product/$',ProductCreateAPIView.as_view(),name='add_product'),
    url(r'^list/products/$',ProductListAPIView.as_view(),name='list_product'),
    url(r'^detail/product/(?P<id>\d+)/$',ProductDetailAPIView.as_view(),name='detail_product'),
    url(r'^buy/$',SaleCreateAPIView.as_view(),name='buy'),
    url(r'user/purchases/$',UserPurchaseListAPIView.as_view(),name='user_purchase'),
    url(r'rate/product/$',RatingAPIView.as_view(),name='rate_product'),
    url(r'delete/product/(?P<id>\d+)/$',DeleteProductAPIView.as_view(),name='delete_product')
    ]