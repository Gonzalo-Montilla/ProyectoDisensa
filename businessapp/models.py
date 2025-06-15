from django.db import models

class BusinessPartner(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    affiliation_date = models.DateField(null=True, blank=True)
    sales_history = models.TextField(null=True, blank=True)

    def calculate_sales_history(self):
        from django.db.models import Sum
        total = Client.objects.filter(business_partner=self).aggregate(total=Sum('purchase_value'))['total']
        return total if total else 0.00

    def __str__(self):
        return self.name

class Client(models.Model):
    name = models.CharField(max_length=100)
    identification = models.CharField(max_length=20, unique=True, null=True, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    purchase_date = models.DateField()
    purchase_value = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.CharField(max_length=100, null=True, blank=True)  # Permitir nulos temporalmente  # Sin null=True ni blank=True
    business_partner = models.ForeignKey(BusinessPartner, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name