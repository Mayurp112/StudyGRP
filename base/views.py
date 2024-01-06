from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Room,Topic
from .forms import RoomForm 
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

def home(request):
    
    q=request.GET.get('q') if request.GET.get('q') != None else ""

    room=Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
    room_count=room.count()
    
    topic=Topic.objects.all()    
    context={'room':room,'topic':topic,'room_count':room_count}
    
    return render(request,'base/home.html',context)

def room(request,pk):
    room=Room.objects.get(id=pk)
    context={'room':room}
    return render(request,"base/room.html",context)

@login_required(login_url='/login')
def createroom(request):
    form=RoomForm()
    if request.method == 'POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    context={'form':form}
    return render(request,"base/room_form.html",context)



@login_required(login_url='/login')
def updateroom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse(" You can't update this room")

    if request.method == "POST":
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")

    context={'form':form}
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

def login_page(request):

    page='login'


    if request.user.is_authenticated:
        return redirect('home')

    if request.method =="POST":
        username=request.POST.get('username').lower()
        password=request.POST.get('password')

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request," Username does not exist")

        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"  username or password does not exist")

    context={'page':page}
    return render(request,"base/login_register.html",context)

def logoutuser(request):
    logout(request)
    return redirect('home')

def registerpage(request):

    page= 'register'
    form= UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)

        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Error Occure During Registration")

    context={'page':page,'form':form}
    return render(request,'base/login_register.html',context)