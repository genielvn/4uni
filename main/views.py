from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse
from django.views.generic import (
    ListView
)
from django.utils import timezone
from .forms import ThreadForm, LoginForm, SignupForm, ReplyForm
from main.models import Board, Thread, User, Reply, Role
from django.db.models import Subquery, OuterRef, Value
from django.db.models.functions import Coalesce

def boards(request):
    if not request.user.is_authenticated:
        return redirect('/user/login')

    pagination = request.GET.get('page')

    if request.method == 'GET':
        context = {
            'view': 'main/boards.html',
            'boards': [{'info': board,
                        'thread': Thread.objects.filter(board=board).order_by('-updated_at').first()}
                       for board in Board.objects.all()]
        }
        return render(request, "base.html", context)

def threads(request, board_id):
    if request.method == 'GET':
        context = {
            'view': 'main/threads.html',
            'board': get_object_or_404(Board, board_id=board_id),
            'threads': [{
                'info': thread,
                'reply': Reply.objects.filter(thread=thread, is_deleted=False).order_by('-created_at').first(),
                'reply_count': Reply.objects.filter(thread=thread, is_deleted=False).order_by('-created_at').count()
                } for thread in Thread.objects.filter(board_id=board_id, is_deleted=False).order_by('-updated_at')]
        }

        return render(request, "base.html", context)

def create_thread(request, board_id):
    board = get_object_or_404(Board, board_id=board_id)

    if request.method == "POST":
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.board = board

            # TODO: This is temporary for users
            thread.username = User.objects.get(username="Anonymous")
            thread.save()

            # TODO: Redirect to the thread itself
            return redirect('main:thread', board_id=board_id, thread_id=thread.id)
        else:
            form.add_error('title', "Please specify a title!")
    else:
        form = ThreadForm()

    context = {
        'view': 'main/create-thread.html', 
        'board': board,
        'form': form
    }
    return render(request, "base.html", context)

def thread(request, board_id, thread_id):
    board = get_object_or_404(Board, board_id=board_id)
    thread = get_object_or_404(Thread, board=board, id=thread_id, is_deleted=False)

    if request.method == 'POST':
        form = ReplyForm(request.POST)
        
        if form.is_valid():
            reply = form.save(commit=False)
            reply.thread = thread

            # TODO: This is a temporary user
            reply.username = User.objects.get(username="Anonymous")
            reply.save()

            thread.updated_at = timezone.now()
            thread.save()

            return redirect('main:thread', board_id=board_id, thread_id=thread_id)  
        else: 
            form.add_error("body", "Hey, at least specify your reply :<")
    else:
        form = ReplyForm()

        
    context = {
            'view': 'main/thread.html',
            'board': board,
            'thread': thread,
            'replies': Reply.objects.filter(thread_id=thread_id).order_by('created_at'),
            'form': form
        }

    return render(request, 'base.html', context)

def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                print("user auth")
                auth_login(request, user)
                return redirect('/')
            else:
                print("user not auth")
                form.add_error(None, 'Invalid username or password')

    else:
        form = LoginForm()

    return render(request, 'base_user.html', {'view':'main/login.html','form': form})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password1')
            user.set_password(password)
            user.role = Role.objects.get(name='User')
            user.save()

            auth_login(request, user)
            return redirect('/')
        else:
            print('form is invalid')

    else:
        form = SignupForm()

    return render(request, 'base_user.html', {'view':'main/signup.html', 'form': form})

def logout(request):
    auth_logout(request)
    return redirect('/')

def username(request):
    pass
