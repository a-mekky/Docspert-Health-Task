from django.urls import path
from .views import UploadAccountsView, AccountListView, AccountDetailView, TransferFundsView

app_name = 'accounts'

urlpatterns = [
    path('upload/', UploadAccountsView.as_view(), name='upload'),
    path('list/', AccountListView.as_view(), name='list'),
    path('transfer/', TransferFundsView.as_view(), name='transfer'),
    path('<str:account_id>/', AccountDetailView.as_view(), name='detail'),

]
