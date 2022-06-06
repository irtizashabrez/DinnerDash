from django.urls import path
from orders.views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('cart/', CartView.as_view(), name="cart"),
    path('dashboard/', DashBoardView.as_view(), name="dashboard"),
    path('update-order/<int:pk>/', UpdateOrderStatus.as_view(), name='update-order-status'),
    path('dashboard-past-order/<int:pk>/', DasboardPastOrder.as_view(), name='dashboard-past-order'),
    path('dashboard-past-order-detail/<int:pk>/<int:val1>/', DashboardPastOrderDetail.as_view(), name="dashboard-past-order-detail"),
    path('dashboard-order/<int:pk>/', DashboardOrderDetail.as_view(), name='dashboard-order'),
    path('add-item/<int:pk>/', add_to_cart, name="addToCart"),
    path('add/<int:pk>/', add_item_quantity, name="addQuantity"),
    path('minus/<int:pk>/', minus_item_quantity, name="minusQuantity"),
    path('remove-item/<int:pk>/', remove_item_cart, name="removeitemcart"),
    path('add_s/<str:pk>/', add_item_quantity_session, name="addQuantitySession"),
    path('minus_s/<str:pk>/',minus_item_quantity_session , name="minusQuantitySession"),
    path('remove-item_s/<str:pk>/', remove_item_cart_session, name="removeItemSession"),
    path('past-order/', PastOrderView.as_view(), name="pastOrder"),
    path('past-order/<int:pk>/', PastOrderDetail.as_view(), name="pastOrderDetail"),
    path('checkout/', CheckOutView.as_view(), name='checkout'),
]
