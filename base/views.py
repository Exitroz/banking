from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Transaction, OTP
from accounts.models import Account
from .forms import TransferForm
import random
from django.core.mail import EmailMessage, get_connection, send_mail
from django.conf import settings

# Create your views here.
def home(request):
    return render(request, 'welcome.html')


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
                account_name=form.cleaned_data['account_name'],
                account_number=form.cleaned_data['account_number'],
                bank_name=form.cleaned_data['bank_name'],
                amount=form.cleaned_data['amount'],
                otp=otp
            )
            transaction.save()
            # send OTP to user's email
            send_mail(
                "You placed a transfer request",
                str(otp),
                None,
                ["ezeobih@gmail.com"],
                fail_silently=False,
            )
            # with get_connection(  
            # host=settings.EMAIL_HOST, 
            #     port=settings.EMAIL_PORT,  
            #     username=settings.EMAIL_HOST_USER, 
            #     password=settings.EMAIL_HOST_PASSWORD, 
            #     use_tls=settings.EMAIL_USE_TLS  
            #     ) as connection:  
            # subject = request.POST.get("subject")  
            # email_from = settings.EMAIL_HOST_USER  
            # recipient_list = [request.POST.get("email"), ]  
            # message = request.POST.get("message")  
            # EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()
            
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
    account = Account.objects.all()
    context = {'account':account}
    return render(request, 'index.html', context)