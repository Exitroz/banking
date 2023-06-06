from django import forms

class TransferForm(forms.Form):
    account_name = forms.CharField(max_length=255)
    account_number = forms.IntegerField()
    bank_name = forms.CharField(max_length=50)
    amount = forms.FloatField()
    # otp = forms.CharField(max_length=6)
