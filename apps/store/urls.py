from django.urls import path

from . import views  

urlpatterns = [
    path('create-supplier/', views.create_supplier, name='create-supplier'),
    path('create-buyer/', views.create_buyer, name='create-buyer'),
    path('create-season/', views.create_season, name='create-season'),
    path('create-drop/', views.create_drop, name='create-drop'),
    path('create-product/', views.create_product, name='create-product'),
    path('create-order/', views.create_order, name='create-order'),
    path('create-delivery/', views.create_delivery, name='create-delivery'),

    path('delete-buyer/<int:pk>/', views.delete_buyer, name='delete-buyer'),
    path('delete-order/<int:pk>/', views.delete_order, name='delete-order'),

    path('edit-buyer/<int:pk>/', views.edit_buyer, name='buyer_edit'),

    path('supplier-list/', views.SupplierListView.as_view(), name='supplier-list'),
    path('buyer-list/', views.BuyerListView.as_view(), name='buyer-list'),
    path('season-list/', views.SeasonListView.as_view(), name='season-list'),
    path('drop-list/', views.DropListView.as_view(), name='drop-list'),
    path('product-list/', views.ProductListView.as_view(), name='product-list'),
    path('order-list/', views.OrderListView.as_view(), name='order-list'),
    path('order-detail/<int:pk>/', views.order_detail, name='order-detail'),
    path('delivery-list/', views.DeliveryListView.as_view(), name='delivery-list'),

    path('product-edit/<int:pk>/', views.ProductListView.as_view(), name='product_edit'),
    path('product-delete/<int:pk>/', views.ProductListView.as_view(), name='product_delete'),
    
]