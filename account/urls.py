# add url patterns
from django.urls import path
from .views import HomeView, LogoutView, RegisterView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('', HomeView.as_view(), name='home'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
