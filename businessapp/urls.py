from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/login/', permanent=False), name='root'),
    path('login/', auth_views.LoginView.as_view(template_name='businessapp/registration/login.html', next_page='dashboard'), name='login'),
    path('clients/', views.client_list, name='client_list'),
    path('partners/', views.partner_list, name='partner_list'),
    path('create_client/', views.create_client, name='create_client'),
    path('export_clients/', views.export_clients_excel, name='export_clients'),
    path('export_partners/', views.export_partners_excel, name='export_partners'),
    path('logout/', views.logout_view, name='logout'),
    path('create_partner/', views.create_partner, name='create_partner'),
    path('register/', views.register, name='register'),
    path('onboarding/', views.onboarding_status, name='onboarding_status'),
]