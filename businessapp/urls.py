from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('businessapp.urls')),
    path('login/', views.login_view, name='login'),
    path('clients/', views.client_list, name='client_list'),
    path('partners/', views.businesspartner_list, name='businesspartner_list'),
    path('create_client/', views.create_client, name='create_client'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('export_clients/', views.export_clients_excel, name='export_clients'),
    path('export_partners/', views.export_partners_excel, name='export_partners'),
]