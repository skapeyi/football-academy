from django.shortcuts import render
from .models import User
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm, RegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin


class RegisterView(View):
   def get(self, request):
       form = RegisterForm()
       return render(request, 'register.html', {'form': form})
    
   def post(self, request):
         form = RegisterForm(request.POST)
         if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            telephone = form.cleaned_data.get('telephone')
   
            # Create a new user
            user = User.objects.create_user(email=email, password=password)
            user.telephone = telephone
            user.save()
            return redirect('login')
         return render(request, 'register.html', {'form': form})
      

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            # Authenticate user
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home page after successful login
            else:
                form.add_error(None, "Invalid email or password.")
        return render(request, 'login.html', {'form': form})


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'home.html')

class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('login')
