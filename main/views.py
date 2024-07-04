from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.utils import timezone
from .forms import ThreadForm, LoginForm, SignupForm, ReplyForm, BoardForm
from main.models import Board, Thread, User, Reply, Role
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404

@login_required(login_url="main:login")
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

@login_required(login_url="main:login")
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

@login_required(login_url="main:login")
def create_thread(request, board_id):
    board = get_object_or_404(Board, board_id=board_id)

    if request.method == "POST":
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.board = board

            thread.username = request.user
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
    print(request.user)
    return render(request, "base.html", context)

@login_required(login_url="main:login")
def thread(request, board_id, thread_id):
    board = get_object_or_404(Board, board_id=board_id)
    thread = get_object_or_404(Thread, board=board, id=thread_id, is_deleted=False)

    if request.method == 'POST':
        form = ReplyForm(request.POST)
        
        if form.is_valid():
            reply = form.save(commit=False)
            reply.thread = thread

            reply.username = request.user
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

@login_required(login_url="main:login")
def username(request, username):
    context = {
        'view': 'main/user.html',
        'user': get_object_or_404(User, username=username),
        'threads_made': Thread.objects.filter(username=username).order_by('-created_at')
    }
    return render(request, 'base.html', context)

@login_required(login_url="main:login")
def user_settings(request):
    return render(request, 'base.html', {'view':'main/user-settings.html', 'user': request.user})

@login_required(login_url="main:login")
def create_board(request):
    if not request.user.role.name == "Moderator":
        raise Http404
    
    if request.method == 'POST':
        form = BoardForm(request.POST)
        
        if form.is_valid():
            reply = form.save()

            return redirect('main:threads', board_id=reply.board_id)  
        else: 
            form.add_error("board_id", "Duplicate ID!")
    else:
        form = BoardForm()

    context = {
        'view': 'main/create-board.html',
    }

    return render(request, 'base.html', context)
    
def ban_user(request, username):
    if not request.user.role.name == "Moderator":
        raise Http404
    
    user_to_ban = get_object_or_404(User, username=username)
    user_to_ban.is_banned = not user_to_ban.is_banned
    user_to_ban.save()

    return redirect('main:user', username=username)

def delete_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    if not request.user.role.name == "Moderator" and not request.user.username == thread.username.username:
        raise Http404
    
    thread.delete()

    return redirect('main:user', username=thread.username.username)