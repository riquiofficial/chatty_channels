from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .models import ChatRoom, Message


@login_required()
def index(request):
    user = request.user

    if request.method == "POST":
        room = request.POST["room"]
        if room:
            new_room, created = ChatRoom.objects.get_or_create(name=room)
            context = {"message": "Room Created!" if created else "",
                       "room": new_room.name}
            return redirect(f"room/{new_room.id}", context)

    return render(request, "chatty_channels_app/index.html", {"username": user.username})


@login_required()
def room(request, pk):

    try:
        room = ChatRoom.objects.get(pk=pk)
        messages = Message.objects.filter(room=room)

        if request.method == "POST":
            message = request.POST["message"]
            if message:
                Message.objects.create(
                    sender=request.user, room=room, body=message)

        return render(request, "chatty_channels_app/room.html", {"room": room, "chat_messages": messages})
    except ChatRoom.DoesNotExist:
        return redirect("index", {"message": f"Chat room {pk} does not exist."})


@login_required()
def signout(request):

    logout(request)
    return redirect("login")


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
                return redirect("index")
            except:
                return(render(request, "chatty_channels_app/login.html"), {"message": "Login invalid. Please try again"})

        else:
            return render(request, "chatty_channels_app/login.html", {"message": "invalid user"})

    return(render(request, "chatty_channels_app/login.html"))
