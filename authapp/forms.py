# Форма по сути относится ко view, но удобнее и лучше прописывать их в отдельном файле forms.py
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import ShopUser, ShopUserProfile
import random, hashlib


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(ShopUserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'login_field_form'  # это чтобы Bootstrap работал


class ShopUserRegisterForm(UserCreationForm):
    age = forms.IntegerField(label='Age')

    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'password1', 'password2', 'email', 'age', 'avatar',)
        # fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ShopUserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'login_field_form'

            # валидация работает, но ошибку не печатает...

    def clean_image(self):
        image = self.cleaned_data['image']
        if image._size > 4 * 1024 * 1024:
            raise forms.ValidationError("Image file too large ( > 4mb )")
        print(image._size, '+++++++++++++++++++++++++++++')

    def save(self):
        user = super(ShopUserRegisterForm, self).save()

        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.save()

        return user

    # VV метод валидации VV
    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError("Вы слишком молоды и наивны!")
        return data


class ShopUserEditForm(UserChangeForm):
    age = forms.IntegerField(label='Age')
    username = forms.CharField(label='LOGIN')  # Будет отображаться над полем в странице edit

    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'email', 'age', 'avatar', 'password')

    def __init__(self, *args, **kwargs):
        super(ShopUserEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():

            if field_name == 'password':
                field.widget = forms.HiddenInput()

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError("Вы слишком молоды!")

        return data


class ShopUserProfileEditForm(forms.ModelForm):
    class Meta:
        model = ShopUserProfile
        fields = ('tagline', 'aboutMe', 'gender', 'bdate')



    def __init__(self, *args, **kwargs):
        super(ShopUserProfileEditForm, self).__init__(*args, **kwargs)
        # for field_name, field in self.fields.items():
        # field.widget.attrs['class'] = 'form-control'  - подтяжка CSS из Bootstrap (я сам написал, оно мне не надо)
