from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Vote, Item, CartItem, Order, OrderItem

User = get_user_model()


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'title', 'start_datetime', 'end_datetime']


class ItemSerializer(serializers.ModelSerializer):
    size = serializers.StringRelatedField(many=True)

    class Meta:
        model = Item
        fields = ['name', 'size', 'image', 'id']


class CartItemUpdateOrCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['item', 'size', 'quantity']

    def validate_quantity(self, value):
        """ 数量に対するバリデーションメソッド
            数量が0以下の場合は無効にする
            数量が3以上の場合は無効にする"""

        if (value <= 0 or 2 < value):
            raise serializers.ValidationError(
                "数量は1か2にしてください。"
            )
        return value


class CartItemListSerializer(serializers.ModelSerializer):
    size = serializers.StringRelatedField()
    item = ItemSerializer()

    class Meta:
        model = CartItem
        fields = ['item', 'size', 'quantity']


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['id', 'name', 'image']


class OrderHistoryVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['title', 'start_datetime', 'end_datetime', 'status']


class OrderHistoryOrderItemsSerializer(serializers.ModelSerializer):
    item = OrderItemSerializer()
    size = serializers.StringRelatedField()

    class Meta:
        model = OrderItem
        fields = ['item', 'size', 'quantity']


class OrderHistoryOrderSerializer(serializers.ModelSerializer):
    order_items = OrderHistoryOrderItemsSerializer(many=True, read_only=True)
    vote = OrderHistoryVoteSerializer()

    class Meta:
        model = Order
        fields = ['id', 'order_datetime', 'order_items', 'vote']


class CurrentVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'


class OrderItemsSerializer(serializers.ModelSerializer):
    item = OrderItemSerializer()
    size = serializers.StringRelatedField()

    class Meta:
        model = OrderItem
        fields = ['item', 'size', 'quantity']


class OrderItemCountSerializer(serializers.ModelSerializer):
    item = OrderItemSerializer()
    size = serializers.StringRelatedField()

    class Meta:
        model = OrderItem
        fields = ['item', 'size', 'quantity']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']
