from django.db import models
from ..accounts.models import CustomUser


class Size(models.Model):
    size = models.CharField("サイズ", max_length=255, unique=True)

    def __str__(self):
        return self.size

    class Meta:
        verbose_name_plural = "Sizes"


class Item(models.Model):
    size = models.ManyToManyField(Size)
    image = models.ImageField("商品画像", upload_to="item/",)
    name = models.CharField("商品名", max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Items"


class Vote(models.Model):
    title = models.CharField("タイトル", max_length=255)
    start_datetime = models.DateTimeField("開始時間")
    end_datetime = models.DateTimeField("終了時間")
    status_choises = (
        (0, "予約中"),
        (1, "開催中"),
        (2, "終了")
    )
    status = models.IntegerField("状態", choices=status_choises)
    created = models.DateTimeField("作成日時", auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Votes"


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    vote = models.ForeignKey(Vote, on_delete=models.PROTECT)
    order_datetime = models.DateTimeField("購入時間", auto_now_add=True)

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name_plural = "Orders"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    size = models.ForeignKey(Size, on_delete=models.PROTECT)
    quantity = models.IntegerField('数量')

    def __str__(self):
        return '{}:{}'.format(self.order.user.email, self.order.vote.title)

    class Meta:
        verbose_name_plural = "OrderItems"


class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    size = models.ForeignKey(Size, on_delete=models.PROTECT)
    quantity = models.IntegerField('数量')

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name_plural = "CartItems"
