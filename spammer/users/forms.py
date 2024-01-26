from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.sites.shortcuts import get_current_site
from spammer.services import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserProfileForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class UserForgotPasswordForm(StyleFormMixin, PasswordResetForm):
    """
    Запрос на восстановление пароля
    """

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


class UserForgotPasswordNewGenForm(StyleFormMixin, PasswordResetForm):
    """
    Запрос на восстановление пароля
    """

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    def save(
            self,
            from_email=None,
            request=None,
            html_email_template_name=None,
            *args, **kwargs
    ):
        email = self.cleaned_data['email']

        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain

        for user in self.get_users(email):
            new_password = User.objects.make_random_password()
            user.set_password(new_password)
            user.save()

            context = {
                "email": user.email,
                "domain": domain,
                "site_name": site_name,
                "user": user,
                "new_password": new_password
            }

            self.send_mail(
                context=context,
                from_email=from_email,
                to_email=user.email,
                subject_template_name='password_new_gen_message_mail.txt',
                email_template_name='password_reset_new_gen.html',
                html_email_template_name=html_email_template_name,
            )


class UserSetNewPasswordForm(StyleFormMixin, SetPasswordForm):
    """
    Изменение пароля пользователя после подтверждения
    """

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })
