from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages   
from .forms import SignInForm, SignUpForm 

# Create your views here.


def Logout(request):
    logout(request)
    return redirect("login")

def custom_login_view(request):
    form = SignInForm(request.POST or None)
    error_message = None

    if request.method == "POST":
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error_message = "Invalid email or password."
    return render(request, 'cred/login.html', {'form': form, 'error_message': error_message})
        
class SignUpView(View):
    template_name = 'cred/signup.html'

    def get(self, request):
        form = SignUpForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')  # change this to your homepage or dashboard
        return render(request, self.template_name, {'form': form})