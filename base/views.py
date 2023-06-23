from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Transaction, OTP
from accounts.models import Account, User
from .forms import TransferForm
import random
from django.core.mail import EmailMessage, get_connection, send_mail
from django.conf import settings


# Create your views here.
def home(request):
    return render(request, 'welcome.html')


@login_required(login_url='login')
def transfer(request):
    transaction = Transaction.objects.all()
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            # generate OTP
            otp = random.randint(100000, 999999)
            print(otp)
            # store OTP in database
            transaction = Transaction(
                sender=request.user,
                account_name=form.cleaned_data['account_name'],
                account_number=form.cleaned_data['account_number'],
                bank_name=form.cleaned_data['bank_name'],
                amount=form.cleaned_data['amount'],
                otp=otp
            )
            transaction.save()
            # send OTP to user's email
            send_mail(
                "You placed a transfer request, please provide the otp below to verify your transaction",
                str(otp),
                'floydedwards22@gmail.com',
                ["ezeobi888@gmail.com"],
                fail_silently=False,
            )
            
            
            # implement SMS gateway code here
            return redirect('verify-transaction', transaction.id)
    else:
        form = TransferForm()
    context = {'form': form, 'transaction': transaction}
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
            account_name = transaction.account_name
            account_number = transaction.account_number
            bank_name = transaction.bank_name
            amount = transaction.amount
            new_balance = account.balance - amount
            account.balance = new_balance
            
            # sender.balance -= amount
            # receiver.balance += amount
            sender.save()
            account.save()
            # receiver.save()
            # transaction.delete()
            messages.success(request, 'Transaction successful.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid OTP.')
    context = {'transaction': transaction}
    return render(request, 'verify_transaction.html', context)

def dashboard(request):
    transaction = Transaction.objects.all()
    account = Account.objects.all()
    context = {'account':account, 'transaction': transaction}
    return render(request, 'index.html', context)

def about(request):
    context = {}
    return render(request, 'about.html', context)

def contact(request):
    context = {}
    return render(request, 'contact.html', context)

def services(request):
    context = {}
    return render(request, 'services.html', context)

@login_required(login_url='login')
def updateProfile(request, id):
    account = User.objects.get(pk=id)
    if request.method == 'POST':
        account.username = request.POST.get('username')
        account.first_name = request.POST.get('firstname')
        account.last_name = request.POST.get('lastname')
        account.save()
        return redirect('dashboard')
        
    context = {'account': account}
    return render(request, 'settings-profile.html', context)

@login_required(login_url='login')
def profile(request, id):
    account = User.objects.get(pk=id)
    context = {'account': account}
    return render(request, 'profile.html', context)