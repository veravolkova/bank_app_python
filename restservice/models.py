from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db import models
from datetime import timedelta
import decimal

from restservice.utils import get_currency_rate, get_random_id

CURRENCY = (
    (0, 'EUR'),
    (1, 'USD'),
    (2, 'GBP'),
    (3, 'RUB'),
)

TYPE = (
    (0, 'AUTH'),
    (1, 'PRSNT'),
)


class Account(models.Model):
    id = models.IntegerField(primary_key=True, default=get_random_id, editable=False)        
    ledger_balance = models.DecimalField(_('Ledger balance'), max_digits=10, default=0.0, decimal_places=2)
    available_balance = models.DecimalField(_('Available balance'), max_digits=10, default=0.0, decimal_places=2)
    currency = models.PositiveIntegerField(_('Currency'), choices=CURRENCY, default=0)
    create_time = models.DateTimeField(_('Create time'), default=timezone.now)    

    @property
    def currency_type(self):
        return CURRENCY[self.currency][1]   

    def get_coefficient(self, amount, other_currency):
        k = decimal.Decimal(1.0)
        cur_type = self.currency_type
        if cur_type != other_currency:
            k = decimal.Decimal(get_currency_rate(cur_type, other_currency))
        return k

    def check_result(self, amount, other_currency):
        k = self.get_coefficient(amount, other_currency)
        amount = amount * k
        if amount:
            return self.available_balance - amount > 0
        
    def change_ledger_balance(self, force_update=False):
        self.ledger_balance = self.available_balance
        super(Account, self).save(force_update)

    def __str__(self):        
        return  f'ID: {self.id}, {self.available_balance}, {self.currency_type!r}'


class Transaction(models.Model):
    # some fields needed for testing purposes
    id = models.IntegerField(primary_key=True, default=get_random_id, editable=False)
    type = models.PositiveIntegerField(_('Message'), choices=TYPE, default=0) 
    create_time = models.DateTimeField(_('Create time'), default=timezone.now) 
    source_account = models.ForeignKey('Account', related_name='source_account', verbose_name=_('Source Account'),
                                       blank=True, null=True, on_delete=models.CASCADE)
    destination_account = models.ForeignKey('Account', related_name='destination_account', verbose_name=_('Destination Account'),
                                            blank=True, null=True, on_delete=models.CASCADE)
    transaction_amount = models.DecimalField(_('Transaction Amount'), max_digits=10, decimal_places=2)    

    def __str__(self):        
        return  f'ID: {self.id}'
        
        
class Transfer(models.Model):    
    id = models.IntegerField(primary_key=True, default=get_random_id, editable=False)  
    transaction_id = models.ForeignKey('Transaction', related_name='transaction_id', verbose_name=_('Transaction_Id'),
                                       blank=True, null=True, on_delete=models.CASCADE)      
    create_time = models.DateTimeField(_('Create time'), default=timezone.now)    
    transfer_source_account = models.ForeignKey('Account', related_name='transfer_source_account',
                                       verbose_name=_('Transfer Source Account'),
                                       blank=True, null=True, on_delete=models.CASCADE)
    transfer_destination_account = models.ForeignKey('Account', related_name='transfer_destination_account',
                                            verbose_name=_('Transfer Destination Account'),
                                            blank=True, null=True, on_delete=models.CASCADE)
    transfer_amount = models.DecimalField(_('Transfer Amount'), max_digits=10, null=True, decimal_places=2)

