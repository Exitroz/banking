from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('transfer', views.transfer, name='transfer'),
    path('verify-transaction/<int:transaction_id>', views.verify_transaction, name="verify-transaction"),
]

