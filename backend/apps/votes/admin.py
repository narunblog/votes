from django.contrib import admin
from .models import Vote, Order, Item, Size, OrderItem, CartItem

from django.utils.html import format_html


@admin.register(Item)
class Model1Admin(admin.ModelAdmin):

    def image_tag(self, obj):
        return format_html('<img  width="100" height="100" src="{}" />'.format(obj.image.url))

    image_tag.short_description = 'イメージ'

    def _size_tag(self, obj):
        return ','.join([x.size for x in obj.size.all()])

    _size_tag.short_description = 'サイズ'

    list_display = ['name', 'image_tag', '_size_tag']


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ['order_datetime']


admin.site.register(Order, OrderAdmin)
admin.site.register([Vote, Size, OrderItem, CartItem])
