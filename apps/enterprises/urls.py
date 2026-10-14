from django.urls import path
from . import views

urlpatterns = [
    path('create-enterprise/', views.create_enterprise, name='create-enterprise'),
    path('enterprise-list/', views.EnterpriseListView.as_view(), name='enterprise-list'),
    path('edit-enterprise/<int:pk>/', views.edit_enterprise, name='enterprise_edit'),
    path('delete-enterprise/<int:pk>/', views.delete_enterprise, name='delete-enterprise'),
]
