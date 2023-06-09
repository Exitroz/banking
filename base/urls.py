from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('services', views.services, name='services'),
    path('contact', views.contact, name='contact'),
    path('updateprofile/<int:id>', views.updateProfile, name='updateprofile'),
    path('profile/<int:id>', views.profile, name='profile'),
    path('transfer', views.transfer, name='transfer'),
    path('verify-transaction/<int:transaction_id>', views.verify_transaction, name="verify-transaction"),
    path('dashboard', views.dashboard, name="dashboard"),
]

