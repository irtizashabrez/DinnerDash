from django.urls import path
from items.views import *


urlpatterns = [
    path('', DisplayItems.as_view(), name="home"),
    path('create/', AddItem.as_view(), name="create-item"),
    path('add-category/', AddCategory.as_view(), name="add-category"),
    path('<int:pk>/update/', UpdateItem.as_view(), name="update-item"),
    path('item/<int:pk>/', ItemView.as_view(), name="item-detail"),
    path('<int:pk>/delete/', DeleteItem.as_view(), name="delete-item"),
    path('api/', testAPi, name="api"),
    path('api/item-list/', item_json, name="item-list-json"),
    path('api/item-list/<int:pk>/', item_view_json, name="item-list-json"),
    path('api/category-list/', category_json, name="category-list-json"),
]
