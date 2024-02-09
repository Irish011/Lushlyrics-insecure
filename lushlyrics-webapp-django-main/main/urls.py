from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("home", views.home, name='home'),
    path("playlist/", views.playlist, name='your_playlists'),
    path("search/", views.search, name='search_page'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),

]