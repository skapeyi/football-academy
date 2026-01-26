from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import PlaySchedule, Player, PlayerAttendance, User, UserPlayer
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm, PlayScheduleForm, PlayerAttendanceForm, PlayerForm, RegisterForm, UserPlayerForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import timedelta


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
            return redirect('account:login')
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
                return redirect('account:home')  # Redirect to home page after successful login
            else:
                form.add_error(None, "Invalid email or password.")
        return render(request, 'login.html', {'form': form})


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'home.html')

class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('account:login')

# Players
class ListPlayerView(LoginRequiredMixin, View):
    def get(self, request):
        players = Player.objects.all()
        form = PlayerForm()
        
        context = {
            'players': players,
            'form': form
        }
        return render(request, 'players/list.html', context)


class CreatePlayerView(LoginRequiredMixin, CreateView):
    model = Player
    form_class = PlayerForm

    def form_valid(self, form):
        player = form.save(commit=True)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        pass
    
    def get_success_url(self):
        return reverse('account:players')

class DetailPlayerView(LoginRequiredMixin, View):
    def get(self, request, pk):
        player = get_object_or_404(Player, pk=pk)
        assign_schedule = PlayerAttendanceForm(initial={'player': player})
        today = timezone.now().date()
        past_trainings = PlayerAttendance.objects.filter(
            player=player,
            schedule__date__lt=today
        )
        upcoming_trainings = PlayerAttendance.objects.filter(
            player = player,
            schedule__date__gte=today
        )
        context = {
            'player': player,
            'assign_schedule': assign_schedule,
            'upcoming_trainings': upcoming_trainings,
            'past_trainings': past_trainings
        }
        return render(request, 'players/details.html', context)

# Scheduling
class ListPlaySchedule(LoginRequiredMixin, View):
    def get(self, request):
        today = timezone.now().date()
        past = PlaySchedule.objects.filter(date__lt=today).order_by('-date')
        upcoming = PlaySchedule.objects.filter(date__gte=today).order_by('date')
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


class DetailPlaySchedule(LoginRequiredMixin, View):
    def get(self, request, pk):
        schedule = get_object_or_404(PlaySchedule,  pk=pk)
        attendees = PlayerAttendance.objects.filter(
            schedule = schedule
        )
        context = {
            'schedule': schedule,
            'attendees': attendees
        }
        return render(request, 'scheduling/details.html', context)


class AssignPlayerSchedule(LoginRequiredMixin, CreateView):
    model = PlayerAttendance
    form_class = PlayerAttendanceForm

    def get_success_url(self):
        return reverse(
           'account:player-details',
           kwargs={'pk': self.object.player.pk}
        )


class ConfirmAttendanceView(LoginRequiredMixin, View):
    def post(self, request, pk):
        attendance = get_object_or_404(PlayerAttendance, pk=pk)
        attendance.attended = True
        attendance.save()
        return redirect('account:scheduling-details', pk=attendance.schedule.pk)

# Users
class UserListView(LoginRequiredMixin, View):
    def get(self, request):
        parents = User.objects.all()
       
        context = {
            'parents': parents
        }
        return render(request, 'users/list.html', context)
    

class DetailUserView(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        assign_player = UserPlayerForm(initial={'user': user})
        context = {
            'user': user,
            'assign_player': assign_player
        }
        return render(request, 'users/details.html', context)


class AssignUserPlayer(LoginRequiredMixin, CreateView):
    model = UserPlayer
    form_class = UserPlayerForm
    
    def form_valid(self, form):
        assignment = form.save(commit=True)
        return super().form_valid(form)
        
        
    def get_success_url(self):
        return reverse(
            'account:care-takers-details',
            kwargs={'pk': self.object.user.pk}
        )

    
