from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class University(models.Model):
    name = models.CharField(max_length=100)
    verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'University'
        verbose_name_plural = 'Universities'

    def __str__(self):
        return self.name

class Board(models.Model):
    board_id = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(default="A board.", max_length=100, blank=True) # Can be a motto of the university or a simple description of the board.

    # TODO: Add sorting using class Meta

    class Meta:
        verbose_name = 'Board'

    def __str__(self):
        return self.name

class User(AbstractUser):
    username = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=50)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_banned = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    signature = models.TextField(null=True, blank=True)    # nullable, optional

    class Meta:
        verbose_name = 'User'

    def __str__(self):
        return self.username

class Thread(models.Model):
    title = models.CharField(max_length=50)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(null=False, blank=False)
    img = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    # TODO: Add sorting using class Meta

    class Meta:
        verbose_name = 'Thread' # no need for verbose_name_plural (automatic + 's')

    def __str__(self):
        return f'[T] {self.username}: {self.title}'

class Reply(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    body = models.TextField(null=False, blank=False)
    img = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    # TODO: Add sorting using class Meta

    class Meta:
        verbose_name = 'Reply'
        verbose_name_plural = 'Replies'

    def __str__(self):
        return f'[R] {self.username} to {self.thread}: {self.body}'
    
