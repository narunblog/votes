from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Vote, Item, CartItem, Order, OrderItem
from django.db.models import Q


User = get_user_model()


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'title', 'start_datetime', 'end_datetime']

    def validate(self, attr):
        # 予約中の投票や開催中の投票がある場合には、新規作成できないようにする
        vote = Vote.objects.filter(Q(status=0) | Q(status=1))
        if vote:
            raise serializers.ValidationError(
                "予約中の投票や開催中の投票があるため新規作成できません。"
            )

        return attr


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


class OrderRetrieveUpdateListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        order_items = [OrderItem(**order_item,) for order_item in validated_data]
        return OrderItem.objects.bulk_create(order_items)

    def validate(self, attrs):
        # 1つのオーダーに対するアイテムの合計数が2つを超える場合は無効とする
        sum = 0
        for attr in attrs:
            sum += attr['quantity']
        if 2 < sum:
            raise serializers.ValidationError(
                "注文するアイテムの合計数が2を超えました。"
            )
        return attrs


class OrderRetrieveUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['item', 'size', 'quantity']
        list_serializer_class = OrderRetrieveUpdateListSerializer


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['user', 'vote']

    def validate_vote(self, value):
        last_vote = Vote.objects.last()
        # 指定された投票が最新のものではない場合、注文を無効にする
        if (last_vote.id != value.id):
            raise serializers.ValidationError(
                "指定した投票は最新のものではないため注文することができません。"
            )

        # 投票が開始されていない場合、注文を無効とする
        if (last_vote.status == 0):
            raise serializers.ValidationError(
                "指定した投票はまだ開始されていないため、注文することができません。"
            )

        # 投票期限が終了している場合、注文を無効とする
        if (last_vote.status == 2):
            raise serializers.ValidationError(
                "指定した投票は期限が終了しているため、注文することができません。"
            )
        return value
