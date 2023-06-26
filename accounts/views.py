from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404

from .forms import CustomerUserChangeForm, CustomerUserCreationForm
from base.views import home
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
User = get_user_model()

def activate(request, uidb64, token):
    # User = get_user_model()
    # try:
    #     uid = force_str(urlsafe_base64_decode(uidb64))
    #     user = User.objects.get(pk=uid)
    # except:
    #     user = None

    # if user is not None and account_activation_token.check_token(user, token):
    #     user.is_active = True
    #     user.save()

    #     messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
    #     return redirect('login')
    # else:
    #     messages.error(request, "Activation link is invalid!")

    return redirect('homepage')

def activateEmail(request, user, to_mail):
    mail_subject = "Activate your user account."
    message = render_to_string("template_active_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_mail])
    if email.send():
        messages.success(request, f'Dear {user}, please go to your email {to_mail} and click on the \
            acivation link to confirm and complete registration, Note check your spam folder.')
        # return redirect('login')
    else:
         messages.error(request, f'Problem sending email to {to_mail}, check if you typed it correctly.')

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
            return render(request, 'signup.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Your Email, ' + email + ',  Already Exists. Please Try Another Email')
            return render(request, 'signup.html')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Your Username, ' + username + ', Already Exists. Please Try Another Username')
            return render(request, 'signup.html')


        if password != password1:
            messages.error(request, "Your passwords Don't match")
            return render(request, 'signup.html')
        user = User.objects.create_user(email=email, first_name=first_name, last_name=last_name, 
                                    username=username, password=password)
        user.save()
        activateEmail(request, user, email)
        
        context = {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'username': username
        }
        
        return redirect('home')
    return render(request, 'signup.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        email = email.strip().lower()
        if ('@' not in email) or (email[-4:] not in '.com.org.edu.gov.net'):
            messages.error(request, 'Your Email, ' + email +', Is Invalid!')
            return render(request, 'signin.html')
        if not User.objects.filter(email=email).exists():
            messages.error(request, 'This email' + email + ', Does Not exists...')
            return render(request, 'signin.html')
        else:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Username or password does not exist')
    return render(request, 'signin.html')



def user_logout(request):
    logout(request)
    return redirect('home')
                