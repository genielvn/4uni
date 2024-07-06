from django.urls import path
from . import views

urlpatterns = [
    path("", views.boards, name='boards'),
    path("<str:board_id>/", views.threads, name='threads'),
    path("<str:board_id>/create/", views.create_thread, name='create_thread'),
    path("<str:board_id>/<int:thread_id>/", views.thread, name='thread'),
    path("user/login/", views.login, name='login'),
    path("user/signup/", views.signup, name='signup'),
    path("user/logout/", views.logout, name='logout'),
    path("user/settings/", views.user_settings, name='user_settings'),
    path("user/<str:username>/", views.username, name='user'),
    path("manage/createboard/", views.create_board, name='create_board'),
    path("manage/ban/<str:username>", views.ban_user, name='ban_user'),
    path("manage/deletethread/<int:thread_id>", views.delete_thread, name='delete_thread'),
    path("manage/deletereply/<int:reply_id>", views.delete_reply, name='delete_reply'),
    path("manage/deleteuser/<str:username>", views.delete_user, name='delete_user'),
    path("manage/editthread/<str:board_id>/<int:thread_id>", views.edit_thread, name='edit_thread')
]
