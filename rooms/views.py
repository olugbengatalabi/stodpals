from multiprocessing import context
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Room, Topic, Message
from .forms import RoomForm
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import get_user_model

def index(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q))[0:3]

    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'pages/index.html', context)



def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, 'rooms/room.html', context)


def userProfile(request, pk):
    user_obj= get_user_model()
    user = get_object_or_404(user_obj, id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        'user': user, 'rooms': rooms,
        'room_messages': room_messages, 'topics': topics
        }
    return render(request, 'account/profile.html', context)


@login_required(login_url='account_login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'rooms/room_form.html', context)


@login_required(login_url='account_login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'room_form.html', context)


@login_required(login_url='account_login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'rooms/delete.html', {'obj': room})


@login_required(login_url='account_login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'rooms/delete.html', {'obj': message})


@login_required(login_url='account_login')
def updateUser(request):
    user = request.user
    if request.method == "POST":
        bio = request.POST['bio']
        try:
            avatar = request.FILES["avatar"]
            fs = FileSystemStorage()
            filename = fs.save(avatar.name, avatar)
            upload_file_url = fs.url(filename)
                            
            if filename != "" and filename is not None:
                user.userprofile.avatar = filename
                user.userprofile.save()
                
        except:
            pass
        
        if bio != "" and bio is not None:
            user.userprofile.bio = bio
            user.userprofile.save()
            messages.success(request, "updated")
        else:
            messages.error(request, "bio cannot be empty")

    else:
        bio = user.userprofile.bio
        if not bio:
            bio = "Bio"
    
    context = {"old_bio":bio}
            
            

        
    # user = request.user
    # # form = UserForm(instance=user)

    # if request.method == 'POST':
    #     form = UserForm(request.POST, request.FILES, instance=user)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('user-profile', pk=user.id)

    return render(request, 'account/update-user.html',context)


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'rooms/topics.html', {'topics': topics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'account/activity.html', {'room_messages': room_messages})
