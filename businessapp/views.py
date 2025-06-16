from django.shortcuts import render, redirect
from .models import Client, BusinessPartner
from django.contrib.auth import authenticate, login
import pandas as pd
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from openpyxl import Workbook
from django.utils.dateformat import format
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from businessapp.models import Client, BusinessPartner
from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import Client, BusinessPartner
import csv
from django.db.models import Sum
from .models import BusinessPartner
from django.db.models import Exists, OuterRef
from .models import BusinessPartner, Client
from django.contrib.auth.forms import UserCreationForm



@login_required
def dashboard(request):
    # Contar socios activos
    active_partners = BusinessPartner.objects.annotate(
        is_active=Exists(Client.objects.filter(business_partner=OuterRef('pk')))
    ).filter(is_active=True).count()
    
    # Total de socios
    total_partners = BusinessPartner.objects.count()
    
    # Total de clientes (asumiendo que Client es el modelo correcto)
    total_clients = Client.objects.count()
    
    # Clientes nuevos (ejemplo: clientes creados en los últimos 30 días)
    from django.utils import timezone
    thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
    new_clients = Client.objects.filter(created_at__gte=thirty_days_ago).count()
    
    # Ingresos totales (suma de purchase_value de todos los clientes)
    total_revenue = Client.objects.aggregate(total=Sum('purchase_value'))['total'] or 0.00

    context = {
        'clients': total_clients,
        'partners': total_partners,
        'new_clients': new_clients,
        'total_revenue': total_revenue,
        'active_partners': active_partners,  # Cambiado de active_partners_count a active_partners para coincidir con la plantilla
    }
    return render(request, 'businessapp/dashboard.html', context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
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
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'businessapp/login.html')

@login_required
def create_client(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        identification = request.POST.get('identification')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        purchase_date_str = request.POST.get('purchase_date')
        purchase_date = parse_date(purchase_date_str) if purchase_date_str else None
        purchase_value = request.POST.get('purchase_value')
        city = request.POST.get('city')
        partner_id = request.POST.get('business_partner')
        business_partner = BusinessPartner.objects.get(id=partner_id) if partner_id else None
        if name and identification and email and phone and purchase_date and purchase_value and city:
            Client.objects.create(
                name=name,
                identification=identification,
                email=email,
                phone=phone,
                purchase_date=purchase_date,
                purchase_value=purchase_value,
                city=city,
                business_partner=business_partner
            )
            return redirect('client_list')
    partners = BusinessPartner.objects.all()
    return render(request, 'businessapp/create_client.html', {'partners': partners})



@login_required
def export_clients_excel(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="clientes.xlsx"'
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Clientes'
    headers = ['Nombre', 'Identificación', 'Fecha de Compra', 'Valor de Compra', 'Ciudad', 'Socio Comercial']
    worksheet.append(headers)
    clients = Client.objects.all()
    for client in clients:
        row = [
            client.name,
            client.identification if client.identification else '',
            format(client.purchase_date, 'd/m/Y') if client.purchase_date else '',
            str(client.purchase_value) if client.purchase_value else '',
            client.city if client.city else '',
            client.business_partner.name if client.business_partner else ''
        ]
        worksheet.append(row)
    workbook.save(response)
    return response
@login_required
def export_partners_excel(request):
    if not request.user.is_authenticated:
        return redirect('login')
    partners = BusinessPartner.objects.all()
    df = pd.DataFrame(list(partners.values('name', 'city', 'affiliation_date', 'sales_history')))
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="partners.xlsx"'
    df.to_excel(response, index=False)
    return response

@login_required
def create_partner(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        city = request.POST.get('city')
        affiliation_date = request.POST.get('affiliation_date')
        sales_history = request.POST.get('sales_history')
        BusinessPartner.objects.create(name=name, city=city, affiliation_date=affiliation_date, sales_history=sales_history)
        return redirect('partner_list')
    return render(request, 'businessapp/create_partner.html')

@login_required
def partner_list(request):
    partners = BusinessPartner.objects.all()
    return render(request, 'businessapp/partner_list.html', {'partners': partners})

@login_required
def export_partners(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="partners.csv"'
    writer = csv.writer(response)
    writer.writerow(['Nombre', 'Ciudad', 'Fecha de Afiliación', 'Historial de Ventas'])
    partners = BusinessPartner.objects.all()
    for partner in partners:
        writer.writerow([partner.name, partner.city, partner.affiliation_date, partner.calculate_sales_history()])
    return response

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso! Bienvenido a CrediSmart.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Hubo un error al registrar. Por favor, verifica los datos.')
    else:
        form = UserCreationForm()
    return render(request, 'businessapp/register.html', {'form': form})

