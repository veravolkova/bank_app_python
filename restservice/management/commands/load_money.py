from django.core.management import BaseCommand, CommandError 
from django.utils import timezone
from datetime import timedelta
import decimal

from restservice.models import Account, Transaction, Transfer
from restservice.utils import get_random_id 

INTR = 0.005


def load_money():  
    #HARD-CODED time for testing
    time1 = timezone.now() - timedelta(days=1)
    time2 = timezone.now() + timedelta(days=1)
    transaction_amount = 0
    transfer_amount = 0       
    
    business_account = Account.objects.filter(id=55843787)[:1].get()    
    queryset_transactions = Transaction.objects.filter(create_time__gt=time1,
                                                      create_time__lte=time2, type=1)             
      
    for trans in queryset_transactions:
        k = trans.source_account.get_coefficient(trans.transaction_amount,
                                                trans.destination_account.currency_type)             
        amount_prsnt = trans.transaction_amount * k        
        revenue = round(decimal.Decimal(amount_prsnt) * decimal.Decimal(INTR), 2)         
        settlement_amount = amount_prsnt - revenue
        
        if revenue and settlement_amount:  
        # transfer to the scheme    
            business_account.available_balance += revenue
            Transfer.objects.create(id=get_random_id(), transaction_id=trans, create_time=time2,
                                transfer_source_account=business_account,
                                transfer_amount=settlement_amount)      


class Command(BaseCommand):
    help = 'Send money to the Scheme'    
    
    def handle(self, **options):        
        load_money()