from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import (
    ListView
)

from .forms import ThreadForm, CommentForm
from main.models import Board, Thread, User, Reply

board = [
    {
        'board_id':'r',
        'name': "Random"
    },
    {
        'board_id':'pup',
        'name': "Polytechnic University of The Philippines"
    },
    {
        'board_id':'up',
        'name': "University of The Philippines"
    },
    {
        'board_id':'ust',
        'name': "University of Santo Tomas"
    },

]

thread = [
    {
        "title": "La Salle Kanal Humor daw",
        "description": "Ano say niyo dito? Ang funny diba? xD"
    }
]

thread_topic = {
    "title": "La Salle Kanal Humor daw",
    "description": "Ano say niyo dito? Ang funny diba? xD",
    "comments": [
        "cringe ampota",
        "why are you here, anon",
        "lmao normie and cringe joke, op thought he has good humor",
        "9/11 jokes are better than this"
    ]
}

# Create your views here.
def boards(request):
    pagination = request.GET.get('page')

    if request.method == 'GET':
        context = {
            'view': 'main/boards.html',
            'boards': Board.objects.all()
        }
        return render(request, "base.html", context)

def threads(request, board_id):
    # pagination = request.GET.get('page')
    # if board_id not in Board.objects.values_list('id', flat=True):
    if request.method == 'GET':
        context = {
            'view': 'main/threads.html',
            'board_id': board_id,
            'board': get_object_or_404(Board, board_id=board_id),
            'threads': Thread.objects.filter(board_id=board_id)
        }

        return render(request, "base.html", context)

def create_thread(request, board_id):
    board = get_object_or_404(Board, board_id=board_id)

    context = {
        'view': 'main/create-thread.html', 
        'board_id': board_id, 
        'board_name': board.name
    }

    if request.method == "GET":
        return render(request, "base.html", context)
    elif request.method == "POST":
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.board = board

            # TODO: This is temporary for users
            thread.username = User.objects.filter(username="Anonymous")[0]
            thread.save()

            # TODO: Redirect to the thread itself
            return redirect('main:threads', board_id=board_id)
        

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

            return redirect('main:post', board_id=board_id, thread_id=thread_id)
