from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Transaction
from .forms import TransferForm
import random

# Create your views here.
def home(request):
    return render(request, 'home.html')


def transfer(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            # generate OTP
            otp = random.randint(100000, 999999)
            # store OTP in database
            transaction = Transaction(
                sender=request.user,
                receiver=form.cleaned_data['receiver'],
                amount=form.cleaned_data['amount'],
                otp=otp
            )
            transaction.save()
            # send OTP to user's mobile number
            # implement SMS gateway code here
            return redirect('verify_transaction', transaction.id)
    else:
        form = TransferForm()
    context = {'form': form}
    return render(request, 'transfer.html', context)

def verify_transaction(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if otp == transaction.otp:
            # execute transaction
            sender = transaction.sender
            receiver = transaction.receiver
            amount = transaction.amount
            sender.balance -= amount
            receiver.balance += amount
            sender.save()
            receiver.save()
            transaction.delete()
            messages.success(request, 'Transaction successful.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid OTP.')
    context = {'transaction': transaction}
    return render(request, 'verify_transaction.html', context)
