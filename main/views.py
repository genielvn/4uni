from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse
from django.views.generic import (
    ListView
)
from django.utils import timezone
from .forms import ThreadForm, LoginForm, SignupForm, ReplyForm
from main.models import Board, Thread, User, Reply
from django.db.models import Subquery, OuterRef, Value
from django.db.models.functions import Coalesce

def boards(request):
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
    # pagination = request.GET.get('page')
    # if board_id not in Board.objects.values_list('id', flat=True):

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

    context = {
        'view': 'main/create-thread.html', 
        'board': board
    }

    if request.method == "GET":
        return render(request, "base.html", context)
    elif request.method == "POST":
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.board = board

            # TODO: This is temporary for users
            thread.username = User.objects.get(username="Anonymous")
            thread.save()

            # TODO: Redirect to the thread itself
            return redirect('main:thread', board_id=board_id, thread_id=thread.id)
        
def thread(request, board_id, thread_id):
    board = get_object_or_404(Board, board_id=board_id)
    thread = get_object_or_404(Thread, board=board, id=thread_id, is_deleted=False)

    if request.method == 'GET':
        context = {
            'view': 'main/thread.html',
            'board': board,
            'thread': thread,
            'replies': Reply.objects.filter(thread_id=thread_id).order_by('created_at')
            }

        return render(request, 'base.html', context)
        
    
    elif request.method == 'POST':
        form = ReplyForm(request.POST)
        
        # TODO: This is temporary for users
        if form.is_valid():
            reply = form.save(commit=False)
            reply.thread = thread

            # TODO: This is a temporary user
            reply.username = User.objects.get(username="Anonymous")
            reply.save()

            thread.updated_at = timezone.now()
            thread.save()

            return redirect('main:thread', board_id=board_id, thread_id=thread_id)  

def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            print(f'form is valid')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(f'{username=} {password=}')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                print('Logged in')
                return redirect('/')
            else:
                print('Invalid username or password')
                form.add_error(None, 'Invalid username or password')
        else:
            print(f'form is invalid! {form.errors=}')

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('/')

    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('/')

def username(request):
    pass
