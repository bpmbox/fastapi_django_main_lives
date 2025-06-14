from django import forms
from .models import Customer, BankAccount, Product

class CustomerForm(forms.ModelForm):
        class Meta:
            model = Customer
            fields = ('full_name', 'furigana', 'phone_number', 'email', 'address', 'id_number', 'id_type')

    class BankAccountForm(forms.ModelForm):
        class Meta:
            model = BankAccount
            fields = ('bank_name', 'branch_name', 'account_number')

    class ProductForm(forms.ModelForm):
        class Meta:
            model = Product
            fields = ('product_type', 'weight', 'serial_number', 'price')

    class OrderForm(forms.Form):
        payment_method = forms.ChoiceField(choices=[(1, 'Cash'), (2, 'Credit Card'), (4, 'Sell Replace')])
        total_price = forms.FloatField()