from django import forms

from accounts.models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'transaction_code']
        # or: exclude = ['profile', 'transaction_time']
