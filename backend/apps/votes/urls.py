from django.urls import path
from .views import (VoteCreateAPIView, ItemListAPIView, ItemRetrieveAPIView, CartItemUpdateOrCreateAPIView,
                    CartItemListAPIView, OrderRetrieveUpdateAPIView, OrderHistoryListAPIView, CurrentVoteOrderAPIView,
                    CurrentVoteAPIView, OrderItemAPIView, OrderItemGenericAPIView, VoteListAPIView, UserListAPIView, MyUserGenericAPIView)

urlpatterns = [
    path('create/', VoteCreateAPIView.as_view()),
    path('item/', ItemListAPIView.as_view()),
    path('item/cart/', CartItemUpdateOrCreateAPIView.as_view()),
    path('item/cart/all/', CartItemListAPIView.as_view()),
    path('item/<int:pk>/', ItemRetrieveAPIView.as_view()),
    path('item/cart/checkout/', OrderRetrieveUpdateAPIView.as_view()),
    path('order/history/', OrderHistoryListAPIView.as_view()),
    path('order/current/', CurrentVoteOrderAPIView.as_view()),
    path('order/item/count/', OrderItemGenericAPIView.as_view()),
    path('order/', OrderItemAPIView.as_view()),
    path('vote/current/', CurrentVoteAPIView.as_view()),
    path('vote/', VoteListAPIView.as_view()),
    path('user/my/', MyUserGenericAPIView.as_view()),
    path('user/', UserListAPIView.as_view()),
]
