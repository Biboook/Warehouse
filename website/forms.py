from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from website.models import User, Store, Product, Expense, Arrival
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ('username', 'password')

    def __int__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for field_name, filed in self.fields.items():
            filed.widget.attrs['class'] = 'input'

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())


class UserRegistrationForm(UserCreationForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

    def __int__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for field_name, filed in self.fields.items():
            filed.widget.attrs['class'] = 'input'

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())


class UserPageForm(UserChangeForm):
    email = forms.CharField(widget=forms.TextInput(attrs={'readonly': True}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def __int__(self, *args, **kwargs):
        super(UserPageForm, self).__init__(*args, **kwargs)
        for field_name, filed in self.fields.items():
            filed.widget.attrs['class'] = 'input'


class StoreForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput())

    class Meta:
        model = Store
        fields = ['name']


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'numbers', 'store'] # added store


class ExpenseForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.none(), widget=forms.Select(attrs={'class': 'form-control'}))
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}))
    destination = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        store = kwargs.pop('store')
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(store=store)
        self.fields['product'].empty_label = '---Select Product---'

    class Meta:
        model = Expense
        fields = ('product', 'quantity', 'destination')

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        quantity = cleaned_data.get('quantity')
        if product and quantity:
            if quantity > product.numbers:
                raise forms.ValidationError('Requested quantity exceeds the available stock.')
        return cleaned_data


class ArrivalForm(forms.ModelForm):

    class Meta:
        model = Arrival
        fields = ['product', 'quantity', 'store']
        widgets = {
            'store': forms.HiddenInput(),
        }


