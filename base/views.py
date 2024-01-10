from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Room,Topic,message,User
from .forms import RoomForm , UserForm,MyUserCreationForm
from django.db.models import Q

from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

def home(request):
    
    q=request.GET.get('q') if request.GET.get('q') != None else ""

    room=Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
    room_count=room.count()
    room_messages=message.objects.all()
    
    topic=Topic.objects.all()    
    context={'room':room,'topic':topic,'room_count':room_count,'room_messages':room_messages}
    
    return render(request,'base/home.html',context)

def room(request,pk):
    room=Room.objects.get(id=pk)
    room_messages=room.message_set.all().order_by('-created_at')
    participants = room.participants.all()
    print(participants)

    if request.method == 'POST':
        Message = message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)



    context={'room':room,'room_messages':room_messages,'participants':participants}
    return render(request,"base/room.html",context)

@login_required(login_url='/login')
def createroom(request):
    form=RoomForm()
    topics=Topic.objects.all()
    if request.method == 'POST':
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        #form=RoomForm(request.POST)
        #if form.is_valid():
        #    room = form.save(commit=False)
        #    room.host=request.user
        #    room.save()
        return redirect("home")
    context={'form':form,'topics':topics}
    return render(request,"base/room_form.html",context)



@login_required(login_url='/login')
def updateroom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    topics=Topic.objects.all()

    if request.user != room.host:
        return HttpResponse(" You can't update this room")

    if request.method == "POST":
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        room.name=request.POST.get('name')
        room.topic=topic
        room.description=request.POST.get('description')
        room.save()
        #form=RoomForm(request.POST,instance=room)
        #if form.is_valid():
        #    form.save()
        return redirect("home")

    context={'form':form,'topics':topics}
    return render(request,"base/room_form.html",context)

@login_required(login_url='/login')
def deleteroom(request,pk):
    room=Room.objects.get(id=pk)


    if request.user != room.host:
        return HttpResponse(" You can't update this room")

    if request.method == 'POST':
        room.delete()
        return redirect("home")
    return render(request,"base/delete.html",{'obj':room})

@login_required(login_url='/login')
def deletemessage(request,pk):
    message=message.objects.get(id=pk)


    if request.user != message.user:
        return HttpResponse(" You can't update this room")

    if request.method == 'POST':
        message.delete()
        return redirect("room")
    return render(request,"base/delete.html",{'obj':message})


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutuser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form': form})

def userProfile(request,pk):
    user=User.objects.get(id=pk)

    room=user.room_set.all()
    room_messages=user.message_set.all()
    topic=Topic.objects.all()

    context={'user':user,'room':room,'room_messages':room_messages,'topic':topic}
    return render(request,'base/profile.html',context)

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})


@login_required(login_url='login')

def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})

