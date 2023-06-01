from django import forms

class TransferForm(forms.Form):
    receiver_name = forms.CharField(max_length=255)
    receiver_number = forms.IntegerField()
    amount = forms.FloatField()
    # otp = forms.CharField(max_length=6)
