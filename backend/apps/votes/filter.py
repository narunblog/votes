import django_filters
from .models import OrderItem


class OrderItemFilter(django_filters.FilterSet):
    order__order_datetime = django_filters.DateTimeFromToRangeFilter()

    class Meta:
        model = OrderItem
        fields = ['order__vote', 'order__user', 'order__order_datetime', 'item', 'size', 'quantity']
