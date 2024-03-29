from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import UserProfile

class Login():
    def __init__(self, email, password, request):
        self.email = email
        self.password = password
        self.request = request

    def verified(self):
        user = authenticate(username=self.email, password=self.password)
        if user:
            login(self.request, user)
            return user.id
        return False


class SignUp():
    def __init__(self, email='', password='', first_name='', last_name=''):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name


    def email_exist(self):
        user = User.objects.filter(email=self.email)
        if user:
            return user[0].email
        return False


    def register_user(self):
        if not self.email_exist():
            User.objects.create_user(
                username=self.email,
                password=self.password,
                email=self.email
            )

            account = self.get_account()
            if account:
                user = UserProfile(
                    user_credential=account,
                    first_name=self.first_name, 
                    last_name=self.last_name)
                user.save()


    def get_account(self, id=False):
        user = User.objects.filter(email=self.email)
        if user:
            if id:
                return user[0].id
            return user[0]
        return False