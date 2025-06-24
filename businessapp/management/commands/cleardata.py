from django.core.management.base import BaseCommand
from businessapp.models import Client, BusinessPartner, PartnerOnboarding

class Command(BaseCommand):
    help = 'Clears all test data from the database'

    def handle(self, *args, **options):
        Client.objects.all().delete()
        BusinessPartner.objects.all().delete()
        PartnerOnboarding.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared test data'))