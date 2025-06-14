from django.shortcuts import render, redirect
from .models import Client, BusinessPartner
from django.contrib.auth import authenticate, login
import pandas as pd
from django.http import HttpResponse

def client_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    clients = Client.objects.all()
    return render(request, 'businessapp/client_list.html', {'clients': clients})

def businesspartner_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    partners = BusinessPartner.objects.all()
    return render(request, 'businessapp/businesspartner_list.html', {'partners': partners})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'businessapp/login.html')

def create_client(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        identification = request.POST.get('identification')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        purchase_value = request.POST.get('purchase_value')
        city = request.POST.get('city')
        partner_id = request.POST.get('business_partner')
        business_partner = BusinessPartner.objects.get(id=partner_id) if partner_id else None
        if name and identification and email and phone and purchase_value and city:
            Client.objects.create(
                name=name,
                identification=identification,
                email=email,
                phone=phone,
                purchase_value=purchase_value,
                city=city,
                business_partner=business_partner
            )
            return redirect('client_list')
    partners = BusinessPartner.objects.all()
    return render(request, 'businessapp/create_client.html', {'partners': partners})

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    clients = Client.objects.all()
    partners = BusinessPartner.objects.all()
    return render(request, 'businessapp/dashboard.html', {'clients': clients, 'partners': partners})

def export_clients_excel(request):
    if not request.user.is_authenticated:
        return redirect('login')
    clients = Client.objects.all()
    df = pd.DataFrame(list(clients.values('name', 'identification', 'purchase_date', 'purchase_value', 'city', 'business_partner__name')))
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="clients.xlsx"'
    df.to_excel(response, index=False)
    return response

def export_partners_excel(request):
    if not request.user.is_authenticated:
        return redirect('login')
    partners = BusinessPartner.objects.all()
    df = pd.DataFrame(list(partners.values('name', 'city', 'affiliation_date', 'sales_history')))
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="partners.xlsx"'
    df.to_excel(response, index=False)
    return response