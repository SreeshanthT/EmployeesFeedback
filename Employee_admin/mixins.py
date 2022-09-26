from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View



class LoggedInUser(LoginRequiredMixin, View):
    login_url = 'login-page'