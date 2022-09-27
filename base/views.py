from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Room, Topic, Message
from .forms import RoomForm
# Create your views here.


def login_user(request):
    page = 'login'
    # if user is logged in : restrict login page
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Invalid user')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def register_user(request):
    page = 'register'

    if request.method == 'POST':
        # passing the data that we passed in form
        registerForm = UserCreationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.username = user.username.lower()
            registerForm.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Registration Failed!')

    registerForm = UserCreationForm()
    context = {'page': page, 'form': registerForm}
    return render(request, 'base/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def home(request):
    q = request.GET.get('q')
    q = q if q is not None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(host__username__icontains=q)
    )
    room_count = rooms.count()
    topics = Topic.objects.all()
    comments = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms': rooms, 'room_count': room_count,
               'topics': topics, 'comments': comments}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room_ = Room.objects.get(id=pk)
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room_,
            body=request.POST.get('body')
        )
        message.save()
        room_.participants.add(request.user)
        return HttpResponseRedirect(request.path_info)
    # to follow foreign key backwards
    participants = room_.participants.all()
    comments = room_.message_set.all()
    context = {'room': room_, 'comments': comments,
               'participants': participants}
    return render(request, 'base/room.html', context)

@login_required
def user_profile(request, user_id):
    user_ = User.objects.get(id=user_id)
    rooms = user_.room_set.all()
    comments = user_.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user_, 'rooms': rooms, 'comments': comments, 'topics': topics}
    return render(request, 'base/profile.html', context)


@login_required
def create_room(request):

    # when creating form
    if request.method == 'POST':
        form_submit = RoomForm(request.POST)
        if form_submit.is_valid():
            form_obj = form_submit.save(commit=False)
            form_obj.host = request.user
            form_obj.save()
            return redirect('home')

    form = RoomForm()
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required
def update_room(request, room_id):
    # get instance
    room = Room.objects.get(id=room_id)
    # restricting updation to the owner
    if request.user != room.host:
        return HttpResponse('You are not allowed to update this room!')
    # when updating form
    if request.method == 'POST':
        # for filling the form
        form_update = RoomForm(request.POST, instance=room)
        if form_update.is_valid():
            form_update.save()
            return redirect('home')

    form = RoomForm(instance=room)
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required
def delete_room(request, room_id):
    # get object
    room = Room.objects.get(id=room_id)
    # when deleting room object
    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {'obj': room}
    return render(request, 'base/delete.html', context)


@login_required
def delete_comment(request, room_id, comment_id):
    message = Message.objects.get(id=comment_id)
    if request.user != message.user:
        return HttpResponse('you are not allowed to delete this message')
    if request.method == 'POST':
        message.delete()
        return redirect('room', room_id)
    context = {'obj': message}
    return render(request, 'base/delete.html', context)
