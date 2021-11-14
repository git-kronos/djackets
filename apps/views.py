import stripe
from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import authentication, permissions, status
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Order, Product
from .serializers import (CategorySerializer, MyOrderSerializer,
                          OrderSerializer, ProductSerializer)


# Create your views here.
class LatestProductList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()[0:4]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetail(APIView):
    def get(self, request, category_slug, product_slug, format=None):
        obj = get_object_or_404(
            Product, slug=product_slug, category__slug=category_slug)
        if obj is not None:
            serializer = ProductSerializer(obj)
            return Response(serializer.data)
        return Response({"message": "Object not found"})


class CategoryDetail(APIView):
    def get(self, request, category_slug, format=None):
        obj = get_object_or_404(Category, slug=category_slug)
        if obj is not None:
            serializer = CategorySerializer(obj)
            return Response(serializer.data)
        return Response({"message": "Object not found"})


@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({"products": []})


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def checkout(request):
    serializer = OrderSerializer(data=request.data)

    if serializer.is_valid():
        stripe.api_key = settings.STRIPE_SECRET_KEY
        paid_amount = sum(item.get(
            'quantity') * item.get('product').price for item in serializer.validated_data['items'])
        try:
            stripe.Charge.create(
                amount=int(paid_amount * 100),
                currency="inr",
                description='D-Jackets Charge',
                source=serializer.validated_data['stripe_token']
            )
            serializer.save(user=request.user, paid_amount=paid_amount)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except stripe.error.AuthenticationError as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.StripeError as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def checkout(request):
    serializer = OrderSerializer(data=request.data)

    if serializer.is_valid():
        stripe.api_key = settings.STRIPE_SECRET_KEY
        paid_amount = sum(item.get(
            'quantity') * item.get('product').price for item in serializer.validated_data['items'])
        try:
            stripe.Charge.create(
                amount=int(paid_amount * 100),
                currency="inr",
                description='D-Jackets Charge',
                source=serializer.validated_data['stripe_token']
            )
            serializer.save(user=request.user, paid_amount=paid_amount)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except stripe.error.AuthenticationError as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.StripeError as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderList(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        queryset = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(queryset, many=True)
        return Response(serializer.data)
