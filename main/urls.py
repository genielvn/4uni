from django.urls import path
from . import views

urlpatterns = [
    path("", views.boards, name='boards'),
    path("<str:board_id>/", views.threads, name='threads'),
    path("<str:board_id>/create/", views.create_thread, name='create_thread'),
    path("<str:board_id>/<int:thread_id>/", views.post, name='post'),
]