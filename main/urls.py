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
    path("user/<str:username>/", views.username, name='user'),
    # path("user/settings/", views.user_settings, name='user_settings'),
]
