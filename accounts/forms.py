from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.core.mail import mail_managers
from django.core.mail import mail_admins



# необходимо убрать класс кастомной формы и переопределить стандартную форму allauth
# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(label="Email")
#     first_name = forms.CharField(label="Имя")
#     last_name = forms.CharField(label="Фамилия")
#
#     class Meta:
#         model = User
#         fields = (
#             "username",
#             "first_name",
#             "last_name",
#             "email",
#             "password1",
#             "password2",
#         )

#автоматически добавляем нового пользователя в группу common:
class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        common_users = Group.objects.get(name="common users")
        user.groups.add(common_users)
        send_mail(
            subject='Добро пожаловать в наш интернет-магазин!',
            message=f'{user.username}, вы успешно зарегистрировались!',
            from_email=None,  # будет использовано значение DEFAULT_FROM_EMAIL
            recipient_list=[user.email],
        )
        mail_managers(
            subject='Новый пользователь!',
            message=f'Пользователь {user.username} зарегистрировался на сайте.'
        )
        mail_admins(
            subject='Новый пользователь!',
            message=f'Пользователь {user.username} зарегистрировался на сайте.'
        )

        return user


