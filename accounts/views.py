from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404

from .forms import CustomerUserChangeForm, CustomerUserCreationForm

User = get_user_model()


def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        password1 = request.POST['password1']

        email = email.strip().lower()
        if ('@' not in email) or (email[-4:] not in '.com.org.edu.gov.net'):
            messages.error(request, 'Your Email, ' + email + ', Is invalid!')
            return render(request, 'accounts/signup.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Your Email, ' + email + ',  Already Exists. Please Try Another Email')
            return render(request, 'accounts/signup.html')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Your Username, ' + username + ', Already Exists. Please Try Another Username')
            return render(request, 'accounts/signup.html')


        if password != password1:
            messages.error(request, "Your passwords Don't match")
            return render(request, 'accounts/signup.html')
        User.objects.create_user(email=email, first_name=first_name, last_name=last_name, 
                                    username=username, password=password)
        context = {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'username': username
        }
        return render(request, 'accounts/signup_success.html', context)
    return render(request, 'accounts/signup.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']


        email = email.strip().lower()
        if ('@' not in email) or (email[-4:] not in '.com.org.edu.gov.net'):
            messages.error(request, 'Your Email, ' + email +', Is Invalid!')
            return render(request, 'Accounts/login.html')
        if not User.objects.filter(email=email).exists():
            messages.error(request, 'This email' + email + ', Does Not exists...')
            return render(request, 'accounts/login.html')
        else:
            user = authenticate(request, username=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
    return render(request, 'accounts/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
                