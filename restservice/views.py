from django.http import Http404
from rest_framework import status
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view

import django_filters
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from restservice.models import Account, Transaction, Transfer

from restservice.serializers import (
    AccountSerializer, AccountDetailSerializer, AccountListSerializer,
    TransactionSerializer, TransactionListSerializer,
    TransactionDetailSerializer, TransferSerializer,)


class AccountCreateAPIView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def perform_create(self, serializer):        
        serializer.save()
        

class AccountDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AccountDetailSerializer

    def get_queryset(self):
        return Account.objects.all()


class AccountListAPIView(generics.ListAPIView):  
    queryset = Account.objects.all().order_by('create_time')
    serializer_class = AccountListSerializer    
    
    filter_backends = (SearchFilter, OrderingFilter)    
    ordering_fields = ['create_time']
    search_fields = ['id']     


class TransactionCreateAPIView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer 
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        data = {'error': False, 'data': None}
        is_validated = serializer.is_valid()       

        if is_validated:            
            self.perform_create(serializer)            
            data['data'] = serializer.data                   
            resp_status = status.HTTP_201_CREATED           
        else:
            resp_status = status.HTTP_403_FORBIDDEN
            data['error'] = True
            data['code'] = resp_status
            data['message'] = serializer.errors

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=resp_status, headers=headers) 
     
    
class TransactionFilter(django_filters.FilterSet):
    # input format = 2006-10-25 14:30:59.000200
    create_time = filters.DateTimeFromToRangeFilter()
   
    class Meta:
        model = Transaction
        fields = ['create_time', 'source_account'] 
        
        
class TransactionList(generics.ListAPIView):  
    queryset = Transaction.objects.all().filter(type=1) 
    serializer_class = TransactionListSerializer       
   
    __basic_fields = ('create_time', 'id', 'source_account')
    filter_class = TransactionFilter
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,
                        SearchFilter, OrderingFilter)
    filter_fileds = __basic_fields
    ordering_fields = ['create_time']
    search_fields = ['create_time']

 
class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):    
    serializer_class = TransactionDetailSerializer
 
    def get_queryset(self):
        return Transaction.objects.all()
    

class TransferList(generics.ListCreateAPIView):
    queryset = Transfer.objects.all().order_by('create_time')
    serializer_class = TransferSerializer
 
    def perform_create(self, serializer):
        serializer.save()

 
class TransferDetail(generics.RetrieveDestroyAPIView):
    serializer_class = TransferSerializer
 
    def get_queryset(self):
        return Transfer.objects.all()
        
