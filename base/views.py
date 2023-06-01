from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Transaction, OTP
from accounts.models import Account
from .forms import TransferForm
import random

# Create your views here.
def home(request):
    return render(request, 'home.html')

login_required
def transfer(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            # generate OTP
            otp = random.randint(100000, 999999)
            print(otp)
            # store OTP in database
            transaction = Transaction(
                sender=request.user,
                receiver_name=form.cleaned_data['receiver_name'],
                receiver_number=form.cleaned_data['receiver_number'],
                amount=form.cleaned_data['amount'],
                otp=otp
            )
            transaction.save()
            # send OTP to user's mobile number
            # implement SMS gateway code here
            return redirect('verify-transaction', transaction.id)
    else:
        form = TransferForm()
    context = {'form': form}
    return render(request, 'transfer.html', context)

def verify_transaction(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user = request.user
        if otp == transaction.otp:
            # execute transaction
            account = Account.objects.get(user=user)
            sender = transaction.sender
            receiver_name = transaction.receiver_name
            receiver_number = transaction.receiver_number
            amount = transaction.amount
            new_balance = account.balance - amount
            account.balance = new_balance
            
            # sender.balance -= amount
            # receiver.balance += amount
            sender.save()
            # receiver.save()
            # transaction.delete()
            messages.success(request, 'Transaction successful.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid OTP.')
    context = {'transaction': transaction}
    return render(request, 'verify_transaction.html', context)
