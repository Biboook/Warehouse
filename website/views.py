from django.contrib.auth import logout, update_session_auth_hash, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseNotFound
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.urls import reverse
from website.forms import UserLoginForm, UserRegistrationForm, UserPageForm, StoreForm, ProductForm, ExpenseForm
from django.contrib import auth, messages
from website.models import Store, User, Product, Expense
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from website.tokens import account_activation_token


def index(request):
    context = {
        'title': 'Main page',
        'h1': 'Welcome to Our Site',
    }
    return render(request, 'website/index.html', context)


def activate(requests, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_activa = True
        user.save()

        messages.success(requests, 'Thank you for your email confirmation. Now can login your account.')
        return redirect('auth')
    else:
        messages.error(requests, 'Activation link is invalid!')

    return redirect('home')


def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('website/activate_email.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear {user}, please go to you email {to_email} inbox and click on \
                        received activation link to confirm and complete the registration. Note: Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')


def reg(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return HttpResponseRedirect(reverse('auth'))
        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, "You must pass the reCAPTCHA test")
                    continue

                messages.error(request, error)
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'website/register.html', context)


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('userpage'))

        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, "You must pass the reCAPTCHA test")
                    continue

                messages.error(request, error)

    form = UserLoginForm()
    context = {'form': form}
    return render(request, 'website/login.html', context)


@login_required
def userpage(request):
    if request.method == 'POST':
        form = UserPageForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully registered!')
            return HttpResponseRedirect(reverse('userpage'))
    else:
        form = UserPageForm(instance=request.user)
    context = {'form': form,
               'store': Store.objects.filter(user=request.user),
               'user': User,
               }
    return render(request, 'website/userpage.html', context)


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("home")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Page Not Found</h1>')


@login_required
def passchange(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password has been successfully changed!')
            return HttpResponseRedirect(reverse('auth'))
        else:
            messages.error(request, 'Please correct the errors!')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'website/change-password.html', {'change_form': form})


@login_required
def get_store(request):
    store = Store.objects.filter(user=request.user)
    products = Product.objects.filter(store__user=request.user)
    return render(request, 'website/store.html', {'store': store, 'products':products})


@login_required
def addstore(request):
    if request.method == 'POST':
        store_form = StoreForm(request.POST)
        if store_form.is_valid():
            store = store_form.save(commit=False)
            store.user = request.user
            store.save()
            return HttpResponseRedirect(reverse('store'))
    else:
        store_form = StoreForm()
    return render(request, 'website/create_store.html', {'store_form': store_form})


@login_required
def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(data=request.POST)
        if product_form.is_valid():
            product_form.save()
            return redirect('add_products')
        else:
            return redirect('add_products')
    else:
        stores = Store.objects.filter(user=request.user.id)
        product_form = ProductForm()
    return render(request, 'website/add_products.html', {'stores': stores, 'product_form': product_form})


@login_required
def store_detail(request, pk):
    store = Store.objects.get(pk=pk)
    products = store.product_set.all()
    per_page = 11
    paginator = Paginator(products, per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {'store': store,
               'products': page
               }
    return render(request, 'website/store_detail.html', context)


def edit_store(request, pk):
    store = Store.objects.get(pk=pk)
    if request.method == 'POST':
        form = StoreForm(request.POST, instance=store)
        if form.is_valid():
            form.save()
            return redirect('store_detail', pk=pk)
    else:
        form = StoreForm(instance=store)
    return render(request, 'website/edit_store.html', {'form': form, 'store': store})


def delete_store(request, pk):
    store = Store.objects.get(pk=pk)

    if request.method == 'POST':
        store.delete()
        return HttpResponseRedirect(reverse('store'))

    return render(request, 'website/delete_store.html', {'store': store})


@login_required()
def expense_product(request, store_id):
    user = request.user
    store = get_object_or_404(Store, pk=store_id, user=user)
    products = Product.objects.filter(store=store)
    if request.method == 'POST':
        form = ExpenseForm(user=user, store=store, data=request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']
            receiver = form.cleaned_data['destination']
            if quantity > product.numbers:
                messages.error(request, 'Requested quantity exceeds the available stock.')
                return redirect('expense_product', store_id=store_id)
            product.numbers -= quantity
            product.save()
            expense = form.save(commit=False)
            expense.store = store
            expense.sender = user
            expense.receiver = receiver
            expense.save()
            messages.success(request, 'The product has been expensed.')
            return redirect('store_detail', pk=store_id)
    else:
        form = ExpenseForm(user=user, store=store)
    context = {
        'form': form,
        'store': store,
        'products': products,
    }
    return render(request, 'website/expense_product.html', context)


def expense_history(request, pk):
    user = request.user
    store = get_object_or_404(Store, pk=pk, user=user)
    expenses = Expense.objects.filter(store=store).order_by('-date')
    context = {
        'store': store,
        'expenses': expenses,
    }
    return render(request, 'website/show_expense.html', context)

