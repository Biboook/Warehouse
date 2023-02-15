from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from website.forms import UserLoginForm, UserRegistrationForm, UserPageForm, StoreForm, ProductForm
from django.contrib import auth, messages
from website.models import Store, User, Product


def index(request):
    context = {
        'title': 'Main page',
        'h1': 'Welcome to Our Site',
    }
    return render(request, 'website/index.html', context)


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


def reg(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('auth'))
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'website/register.html', context)


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
    # send all product details including store to sort products by store_id in template
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
def add_product(request): # erased store_id, it will come with post request
    if request.method == 'POST':
        product_form = ProductForm(data=request.POST)
        if product_form.is_valid():
            product_form.save()

            # you do not have store_detail view in urls.py so I redirected to the same page
            return redirect('add_products')
        else:
            return redirect('add_products')
    else:
        stores = Store.objects.filter(user=request.user.id)
        product_form = ProductForm()
    return render(request, 'website/add_products.html', {'stores': stores, 'product_form': product_form})