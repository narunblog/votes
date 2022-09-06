from django.forms.models import model_to_dict
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import VoteSerializer, ItemSerializer, CartItemUpdateOrCreateSerializer, CartItemListSerializer, OrderHistoryOrderSerializer, OrderItemsSerializer, OrderItemCountSerializer, UserSerializer
from .models import Item, CartItem, Size, Order, OrderItem, Vote
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters import rest_framework as filters
from .filter import OrderItemFilter
from django.db.models import Sum
from config.tasks import vote_status_update
from rest_framework.exceptions import NotFound


User = get_user_model()


class VoteCreateAPIView(CreateAPIView):
    serializer_class = VoteSerializer
    #permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = self.request.user
        if self.is_reserve(serializer.validated_data['start_datetime']):
            status = 0
        else:
            status = 1
        serializer.save(status=status, author=user)

        if self.is_reserve(serializer.validated_data['start_datetime']):
            vote_status_update.apply_async(
                (serializer.data['id'],), eta=serializer.validated_data['start_datetime'])
        else:
            vote_status_update.apply_async(
                (serializer.data['id'],), eta=serializer.validated_data['end_datetime'])

    def is_reserve(self, start_datetime):
        if (timezone.now() < start_datetime):
            return True
        else:
            return False


class ItemListAPIView(ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [AllowAny]


class ItemRetrieveAPIView(RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [AllowAny]


class CartItemUpdateOrCreateAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CartItemUpdateOrCreateSerializer

    def post(self, request, *args, **kwargs):
        # サイズが文字列で返ってきているので、foreign keyのpkに変換する
        size = request.data['size']
        queryset = Size.objects.filter(size=size).first()

        if queryset:
            foreign_key = Size.objects.filter(size=size).first().pk
            request.data['size'] = foreign_key
        # シリアライザオブジェクトを作成
        serializer = CartItemUpdateOrCreateSerializer(data=request.data)
        # バリデーションを実行
        serializer.is_valid(raise_exception=True)
        # サイズとアイテムの両方に一致するモデルオブジェクトがなければ登録あれば数量のみ更新する
        obj, created = CartItem.objects.update_or_create(item=serializer.validated_data['item'], size=serializer.validated_data['size'], user=request.user, defaults={
                                                         'quantity': serializer.validated_data['quantity']})

        return Response(serializer.data, status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        # サイズが文字列で返ってきているので、foreign keyのpkに変換する
        size = request.data['size']
        queryset = Size.objects.filter(size=size).first()

        if queryset:
            foreign_key = Size.objects.filter(size=size).first().pk
            request.data['size'] = foreign_key
        # シリアライザオブジェクトを作成
        serializer = CartItemUpdateOrCreateSerializer(data=request.data)
        # バリデーションを実行
        serializer.is_valid(raise_exception=True)
        # サイズとアイテムの両方に一致するモデルオブジェクトがなければ登録あれば数量のみ更新する
        obj = get_object_or_404(CartItem, user=request.user,
                                item=serializer.validated_data['item'], size=serializer.validated_data['size'])
        if obj:
            obj.delete()
        return Response(serializer.data, status.HTTP_201_CREATED)


class CartItemListAPIView(ListAPIView):
    serializer_class = CartItemListSerializer

    def get_queryset(self):
        """
        この View は、ログインしているユーザーの
        すべてのカートアイテムを返します
        """
        return CartItem.objects.filter(user=self.request.user)


class CartCheckOutAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        vote = request.query_params['vote']
        cart_items = CartItem.objects.filter(user=user)
        order = Order.objects.create(user=user, vote=Vote.objects.get(pk=vote))

        for cart_item in cart_items:
            order_item = OrderItem.objects.create(
                order=order, item=cart_item.item, size=cart_item.size, quantity=cart_item.quantity)
            cart_item.delete()
            print('オーダーアイテムを作成しました{}'.format(order_item))

        return Response({'success'}, status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        user = request.user
        vote = request.data['vote']
        order = Order.objects.get(user=user, vote=vote)
        order_items = OrderItem.objects.filter(order=order)
        for order_item in order_items:
            order_item.delete()

        put_items = request.data['putItems']
        for put_item in put_items:
            size = Size.objects.filter(size=put_item['size']).first()
            item = Item.objects.filter(pk=put_item['item']['id']).first()
            order_item = OrderItem.objects.create(
                order=order, item=item, size=size, quantity=put_item['quantity'])

        return Response({'success'}, status.HTTP_201_CREATED)


class OrderHistoryListAPIView(ListAPIView):
    serializer_class = OrderHistoryOrderSerializer

    def get_queryset(self):
        """
        この View は、ログインしているユーザーの
        すべてのオーダーを返します
        """
        return Order.objects.filter(user=self.request.user)


class CurrentVoteOrderAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        vote = Vote.objects.last().id
        current_order = Order.objects.filter(user=user, vote=vote)
        if current_order:
            return Response('true', status.HTTP_200_OK)
        else:
            return Response('false', status.HTTP_200_OK)


class OrderItemAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        vote = request.query_params['vote']
        order = Order.objects.get(user=user, vote=vote)
        order_item = OrderItem.objects.filter(order=order.id)
        # シリアライザオブジェクトを作成
        serializer = OrderItemsSerializer(order_item, many=True, context={'request': request})
        data = serializer.data
        return Response(data, status.HTTP_200_OK)


class CurrentVoteAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        latest_vote = Vote.objects.last()

        if latest_vote is None:
            raise NotFound(detail='データがありません')
        else:
            dict_obj = model_to_dict(latest_vote)
            return Response(dict_obj, status.HTTP_200_OK)


class OrderItemGenericAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemCountSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = OrderItemFilter

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        q = queryset.values('item__name', 'size__size').annotate(Sum('quantity'))

        return Response([q])


class VoteListAPIView(ListAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [AllowAny]


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
