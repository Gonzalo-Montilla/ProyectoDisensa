from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('clients/', views.client_list, name='client_list'),
    path('partners/', views.businesspartner_list, name='businesspartner_list'),
    path('partners/', views.partner_list, name='partner_list'),
    path('create_client/', views.create_client, name='create_client'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('export_clients/', views.export_clients_excel, name='export_clients'),
    path('export_partners/', views.export_partners_excel, name='export_partners'),
    path('logout/', views.logout_view, name='logout'),
    path('create_partner/', views.create_partner, name='create_partner'),
]