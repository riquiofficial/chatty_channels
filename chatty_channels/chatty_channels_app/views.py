from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .models import ChatRoom


@login_required(login_url="/login/")
def index(request):
    user = request.user

    if request.method == "POST":
        room = request.POST["room"]
        new_room, created = ChatRoom.objects.get_or_create(name=room)




    
    
    

@login_required(login_url="/login/")
def signout(request):
    
    logout(request)
    return render(request, "chatty_channels_app/login.html", {"message": "Logged out."})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("index")

    else:
        form = UserCreationForm()

    return render(request, "chatty_channels_app/signup.html", {"form": form})

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            try:
                login(request, user)
            except:
                return(render(request, "chatty_channels_app/login.html"), {"message": "Login invalid. Please try again"})
            
            return render(request, "chatty_channels_app/index.html")
        else:
            return render(request, "chatty_channels_app/login.html", {"message": "invalid user"})

    return(render(request, "chatty_channels_app/login.html"))
