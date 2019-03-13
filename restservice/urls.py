from django.conf.urls import url, include
from django.contrib import admin
from restservice import views

urlpatterns = [       
    url(r'^accounts/$', views.AccountCreateAPIView.as_view(), name='create_account'),
    url(r'^accounts/list$', views.AccountListAPIView.as_view(), name='account_list'),
    url(r'^accounts/(?P<pk>[0-9]+)/$', views.AccountDetailAPIView.as_view(), name='account_balance'),
        
    url(r'^transactions/$', views.TransactionCreateAPIView.as_view(), name='create_transaction'),
    url(r'^transactions/list/$', views.TransactionList.as_view(), name='transaction_list'),
    url(r'^transactions/(?P<pk>[0-9]+)/$', views.TransactionDetail.as_view(), name='transactions_detail'),
    
    url(r'^transfers/list$', views.TransferList.as_view(), name='transfer_list'),
    url(r'^transfers/(?P<pk>[0-9]+)/$', views.TransferDetail.as_view(), name='transfer_detail'),
]
