# add url patterns
from django.urls import path
from .views import CreatePlaySchedule, HomeView, ListPlaySchedule, ListPlayerView, LogoutView, RegisterView, LoginView, UserListView

app_name = 'account'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('', HomeView.as_view(), name='home'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # players
    path('players/', ListPlayerView.as_view(), name='players'),
    # scheduling
    path('play-schedule', ListPlaySchedule.as_view(), name='scheduling'),
    path('play-schedule/create', CreatePlaySchedule.as_view(), name='scheduling-create'),
    # parents
    path('care-takers', UserListView.as_view(), name='care-takers')
]
