from django.shortcuts import render
from django.urls import reverse
from .models import PlaySchedule, Player, User
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm, PlayScheduleForm, PlayerForm, RegisterForm
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

# Players
class ListPlayerView(LoginRequiredMixin, View):
    def get(self, request):
        players = Player.objects.all()
        context = {
            'players': players
        }
        return render(request, 'players/list.html', context)


class CreatePlayerView(LoginRequiredMixin, View):
    model = Player
    form_class = PlayerForm

    def form_valid(self, form):
        pass
    
    def form_invalid(self, form):
        pass
    
    def get_success_url(self, pk):
        pass


# Scheduling
class ListPlaySchedule(LoginRequiredMixin, View):
    def get(self, request):
        past = PlaySchedule.objects.all()
        upcoming = PlaySchedule.objects.all()
        form = PlayScheduleForm()
        
        context = {
            'past': past,
            'upcoming': upcoming,
            'form': form
        }
        return render(request, 'scheduling/list.html', context)

class CreatePlaySchedule(LoginRequiredMixin, CreateView):
    model = PlaySchedule
    form_class = PlayScheduleForm
    
    def form_valid(self, form):
        schedule = form.save(commit=True)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        pass
    
    def get_success_url(self):
         return reverse('account:scheduling')
    

# Users
class UserListView(LoginRequiredMixin, View):
    def get(self, request):
        parents = User.objects.all()
        context = {
            'parents': parents
        }
        return render(request, 'users/list.html', context)
