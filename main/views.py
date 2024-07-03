from django.shortcuts import render, redirect, get_object_or_404
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
                        'thread': Thread.objects.filter(board=board).order_by('-created_at').first()}
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
            'replies': Reply.objects.filter(thread_id=thread_id).order_by('-created_at')
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

def post(request, board_id, thread_id):
    board = get_object_or_404(Board, board_id=board_id)
    thread = get_object_or_404(Thread, id=thread_id, board_id=board_id)
    replies = Reply.objects.filter(thread=thread)

    if request.method == "GET":
        context = {
            'view': 'main/post.html', 
            'board_id': board_id, 
            'board_name': board.name, 
            'thread_topic': thread,
            'replies': replies
        }
        return render(request, "base.html", context)
    
    elif request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.thread = thread

            # TODO: This is temporary for users
            reply.username = User.objects.filter(username="Anonymous")[0]
            reply.save()

            thread.updated_at = timezone.now()
            thread.save()

            return redirect('main:post', board_id=board_id, thread_id=thread_id)
