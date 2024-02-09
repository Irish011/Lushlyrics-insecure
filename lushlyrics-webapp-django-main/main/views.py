from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import playlist_user
from django.urls.base import reverse
from django.contrib.auth import authenticate, login, logout
from youtube_search import YoutubeSearch
import json
from .forms import CustomUserCreationForm

# import cardupdate


f = open('card.json', 'r')
CONTAINER = json.load(f)


@login_required
def home(request):
    global CONTAINER

    if request.method == 'POST':
        add_playlist(request)
        return HttpResponse("")

    song = 'kSFJGEHDCrQ'
    return render(request, 'player.html', {'CONTAINER': CONTAINER, 'song': song})


def playlist(request):
    cur_user = playlist_user.objects.get(username=request.user)
    try:
        song = request.GET.get('song')
        song = cur_user.playlist_song_set.get(song_title=song)
        song.delete()
    except:
        pass
    if request.method == 'POST':
        add_playlist(request)
        return HttpResponse("")
    song = 'kSFJGEHDCrQ'
    user_playlist = cur_user.playlist_song_set.all()
    # print(list(playlist_row)[0].song_title)
    return render(request, 'playlist.html', {'song': song, 'user_playlist': user_playlist})


def search(request):
    if request.method == 'POST':
        add_playlist(request)
        return HttpResponse("")
    try:
        search = request.GET.get('search')
        song = YoutubeSearch(search, max_results=10).to_dict()
        song_li = [song[:10:2], song[1:10:2]]
        # print(song_li)
    except:
        return redirect('/')

    return render(request, 'search.html', {'CONTAINER': song_li, 'song': song_li[0][0]['id']})


def add_playlist(request):
    cur_user = playlist_user.objects.get(username=request.user)

    if (request.POST['title'],) not in cur_user.playlist_song_set.values_list('song_title', ):
        songdic = (YoutubeSearch(request.POST['title'], max_results=1).to_dict())[0]
        song__albumsrc = songdic['thumbnails'][0]
        cur_user.playlist_song_set.create(song_title=request.POST['title'], song_dur=request.POST['duration'],
                                          song_albumsrc=song__albumsrc,
                                          song_channel=request.POST['channel'], song_date_added=request.POST['date'],
                                          song_youtube_id=request.POST['songid'])




def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email')
            user.save()

            # username = form.cleaned_data.get('username')
            # password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=password)
            # if user is not None:
            #     login(request, user)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        user = None

        if '@' in username_or_email:
            try:
                user = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user.username, password=password)
            except User.DoesNotExist:
                pass
        else:
            user = authenticate(request, username=username_or_email, password=password)

        # form = AuthenticationForm(data=request.POST)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            form= AuthenticationForm(request.POST)
            return render(request, 'login.html', {'form': form, 'error': 'Invalid creds'})

    else:
        form=AuthenticationForm()
    return render(request, 'login.html', {'form': form})
    #     if form.is_valid():
    #         user = form.get_user()
    #         login(request, user)
    #         return redirect('home')
    #
    # else:
    #     form = AuthenticationForm()
    # return render(request, 'login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('login')
