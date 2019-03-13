from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator
from rest_framework import generics, permissions
from rest_framework import serializers
from datetime import datetime

from restservice.models import Account, Transaction, Transfer


class AccountSerializer(serializers.ModelSerializer):
    #create_time = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S") 

    class Meta:
        model = Account
        fields = '__all__'       
        extra_kwargs = {            
            'available_balance': {'validators': [MinValueValidator(limit_value=0)]},
            'ledger_balance': {'read_only': True},
            'create_time': {'read_only': True},
            } 
         

class AccountDetailSerializer(AccountSerializer):  
    transactions = serializers.SerializerMethodField()
    
    class Meta:
        model = Account
        fields = ('id', 'available_balance', 'ledger_balance',
                  'currency', 'currency_type', 'transactions')
    
    def get_transactions(self, obj):
        transactions = obj.source_account.all().filter(type=1)
        return TransactionListSerializer(transactions, many=True).data


class AccountListSerializer(AccountSerializer):
    transactions_count = serializers.SerializerMethodField()    

    class Meta:
        model = Account
        fields = ('id', 'available_balance', 'ledger_balance',
                'currency_type', 'create_time', 'transactions_count')

    def get_transactions_count(self, obj):
        return obj.source_account.count() 


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ('id', 'source_account', 'destination_account',
                  'transaction_amount')
        extra_kwargs = {
            'transaction_amount': {'validators': [MinValueValidator(limit_value=0.01)]},
            } 
       
    def is_valid(self, raise_exception=False):
        is_validated = super().is_valid(raise_exception=False)
        if is_validated:            
            source_account = self.validated_data.get('source_account')
            destination_account = self.validated_data.get('destination_account')
            transaction_amount = self.validated_data.get('transaction_amount')            
            
            if (source_account and destination_account):
                result = source_account.check_result(transaction_amount,
                                                    destination_account.currency_type)                
            elif source_account:
                result = source_account.available_balance - transaction_amount > 0                
            if not result:
                self._errors['transaction_amount'] = _('Amount exceeds the limit')
            is_validated = result
        return is_validated

    
class TransactionListSerializer(TransactionSerializer):
    transfers_count = serializers.SerializerMethodField()
    destination = serializers.SerializerMethodField()
    source = serializers.SerializerMethodField()     

    class Meta:
        model = Transaction
        fields = ('id', 'type', 'transaction_amount', 'create_time',
                  'source', 'destination', 'transfers_count')       

    def get_destination(self, obj):
        return str(obj.destination_account)

    def get_source(self, obj):
        return str(obj.source_account)    
    
    def get_transfers_count(self, obj):
        return obj.transaction_id.count() 
    
     
class TransactionDetailSerializer(serializers.ModelSerializer):    
    transfers = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ('id', 'type', 'create_time', 'source_account', 'destination_account',
                'transfers', 'transaction_amount')
        extra_kwargs = { 
            'transaction_amount': {'validators': [MinValueValidator(limit_value=0.01)]},
            'source_account': {'read_only': True},
            'destination_account': {'read_only': True},
            'create_time': {'read_only': True},
        } 

    def get_transfers(self, obj):
        transfers = obj.transaction_id.all()
        return TransferSerializer(transfers, many=True).data        

    
class TransferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transfer
        fields = '__all__'          
        extra_kwargs = {       
            'create_time': {'read_only': True}       
        }  
        
