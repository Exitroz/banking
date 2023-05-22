from django import forms

class TransferForm(forms.Form):
    receiver = forms.CharField(max_length=100)
    amount = forms.FloatField()
    otp = forms.CharField(max_length=6)
