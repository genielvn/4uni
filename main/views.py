from django.shortcuts import render
from django.http import HttpResponse

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
    return render(request, "base.html", {'view': 'main/boards.html', 'boards': board})

def threads(request, board_id):
    # pagination = request.GET.get('page')
    # if board_id not in Board.objects.values_list('id', flat=True):
    if not any(b["board_id"] == board_id for b in board):
        response = render(request, "404.html")
        response.status_code = 404
        return response
    
    # insert getting threads here
    board_name = next((b for b in board if b['board_id'] == board_id), None)
    return render(request, "base.html", {'view': 'main/threads.html', 'board_id': board_id, 'board_name': board_name['name'], 'threads': thread})

def post(request, board_id, thread_id):
    if not any(b["board_id"] == board_id for b in board):
        response = render(request, "404.html")
        response.status_code = 404
        return response
    
    board_name = next((b for b in board if b['board_id'] == board_id), None)
    return render(request, "base.html", {'view': 'main/post.html', 'board_id': board_id, 'board_name': board_name['name'], 'thread_topic': thread_topic})
