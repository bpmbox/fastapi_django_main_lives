from django.shortcuts import render
from .forms import CustomerForm, BankAccountForm, ProductForm, OrderForm
from .models import Customer, BankAccount, Product, Order)

def create_order(request):
            if request.method == 'POST':
                customer_form = CustomerForm(request.POST)
                bank_account_form = BankAccountForm(request.POST)
                product_form = ProductForm(request.POST)
                order_form.is_valid() and customer_form.is_valid() and bank_account_form.is_valid() and product_form.is_valid():
                    customer = customer_form.save()
            bank_account = bank_account_form.save(commit=False)
            bank_account.customer = customer
            bank_account.save()
            product = product_form.save(commit=False)
            product.customer = customer
            product.save()
            order = Order(customer=customer, payment_method=order_form.cleaned_data['payment_method'], total_price=order_form.cleaned_data['total_price'])
            order.save()
            return render(request, 'order_created.html')
    else:
        customer_form = CustomerForm()
        bank_account_form = BankAccountForm()
        product_form = ProductForm()
        order_form = OrderForm()
    return render(request, 'create_order.html', {'customer_form': customer_form, 'bank_account_form': bank_account_form, 'product_form': product_form, 'order_form': order_form})