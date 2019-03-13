from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
import decimal

from restservice.models import Account, Transaction, Transfer
from restservice.utils import get_random_id

INTR = 0.005


@receiver(post_save, sender=Account)
def account_post_save(sender, instance, created, **kwargs):  
    if created:
        instance.change_ledger_balance()    

          
@receiver(post_save, sender=Transaction)
def transaction_post_save(sender, instance, created, **kwargs):   
    if created: 
        global amount             
        source_account = instance.source_account        
        destination_account = instance.destination_account 
        amount = instance.transaction_amount      
                
        if source_account and destination_account:            
            k = source_account.get_coefficient(amount, destination_account.currency_type)
            amount = amount * k                  
                        
            if amount:
                source_account.available_balance -= amount
                source_account.save()                
           
    if not created and instance.type == 1:
        source_account = instance.source_account
        destination_account = instance.destination_account  
        amount_new = instance.transaction_amount
        #HARD-CODED time change
        instance.create_time += timedelta(days=1)
        
        if source_account and destination_account:            
            k = source_account.get_coefficient(amount_new, destination_account.currency_type)
            amount_new = amount_new * k  
            
            if amount_new:       

                if amount_new > amount:
                    source_account.available_balance -= (amount_new - amount)
                elif amount_new < amount:
                    source_account.available_balance += (amount - amount_new)
                source_account.ledger_balance -= amount_new    
                source_account.save()   
                #HARD-CODED business account
                business_account = Account.objects.filter(id=55843787)[:1].get()
                business_account.available_balance -= amount_new
                business_account.save()
              
            
@receiver(post_save, sender=Transfer)
def transfer_post_save(sender, instance, created, **kwargs):  
    if created:
        source_account = instance.transfer_source_account        
  
        if source_account:
            source_account.ledger_balance -= instance.transfer_amount       
            source_account.save() 

