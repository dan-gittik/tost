import os

from django.contrib.auth.models import User
from django.db import models


def __repr__(self):
    return f'{self.first_name} ({self.username} {self.email})'
User.__repr__ = __repr__


@property
def token(self):
    return self.last_name
@token.setter
def token(self, token):
    self.last_name = token
User.token = token


class Exercise(models.Model):

    class Meta:
        ordering = 'order',

    order = models.IntegerField(unique=True)
    title = models.CharField(max_length=256)
    repo_url = models.CharField(max_length=4096)
    instructions_url = models.CharField(max_length=4096)
    publish_date = models.DateField()
    deadline = models.DateField()

    def __str__(self):
        return f'Exercise {self.order}: {self.title}'


class UserExercise:

    def __init__(self, user, exercise):
        self.user = user
        self.exercise = exercise

    def __getattr__(self, key):
        return getattr(self.exercise, key)

    @classmethod
    def all(cls, user, at):
        for exercise in Exercise.objects.filter(publish_date__lte=at):
            yield cls(user, exercise)

    @property
    def submission(self):
        return Submission.objects.filter(user=self.user, exercise=self.exercise).first()

    @property
    def extension(self):
        return Extension.objects.filter(user=self.user, exercise=self.exercise).first()

    @property
    def effective_deadine(self):
        if self.extension:
            return self.extension.deadline
        return self.deadline


class Submission(models.Model):

    class Meta:
        ordering = 'exercise__order', 'user__first_name'
        unique_together = 'user', 'exercise'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='submissions')
    date = models.DateTimeField()
    test_output = models.TextField(null=True)
    test_grade = models.FloatField(null=True)

    def __str__(self):
        return f'{self.exercise} of {self.user}'

    @property
    def cr_penalty(self):
        return None

    @property
    def final_grade(self):
        if not self.cr_penalty:
            return None
        return self.test_grade - self.cr_penalty


class Extension(models.Model):

    class Meta:
        ordering = 'exercise__order', 'user__first_name'
        unique_together = 'exercise', 'user'

    PENDING = 'p'
    DENIED = 'd'
    APPROVED = 'a'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='extensions')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='extensions')
    deadline = models.DateField()
    reason = models.TextField()
    answer = models.TextField(null=True)
    penalty = models.FloatField(null=True)
    status = models.CharField(max_length=1, choices=[
        (PENDING, 'pending'),
        (DENIED, 'denied'),
        (APPROVED, 'approved'),
    ])

    def __str__(self):
        return f'extension for {self.user} on {self.exercise}'


class Entry(models.Model):

    class Meta:
        ordering = 'name',
        unique_together = 'parent', 'name'

    DIRECTORY = 'd'
    FILE = 'f'
    
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='entries')
    type = models.CharField(max_length=1, choices=[
        (DIRECTORY, 'directory'),
        (FILE, 'file'),
    ])
    parent = models.ForeignKey('Entry', on_delete=models.CASCADE, related_name='children', null=True)
    name = models.CharField(max_length=256)
    data = models.TextField(null=True)

    def __str__(self):
        return f'{self.submission}: {self.path}'

    @property
    def path(self):
        path = [self.name]
        parent = self.parent
        while parent:
            path.append(parent.name)
            parent = parent.parent
        return os.sep.join(path)


class Note(models.Model):

    class Meta:
        ordering = 'line',
        unique_together = 'entry', 'line'

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='notes')
    text = models.TextField()
    line = models.IntegerField(default=0)
    penalty = models.FloatField(null=True)

    def __str__(self):
        return f'note on {self.entry}: {self.text}'


class Post(models.Model):

    class Meta:
        ordering = '-created',
    
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=4096)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    content = models.TextField()
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.author}: {self.title}'

    @property
    def num_comments(self):
        return self.comments.filter(author__is_staff=False).count()

    @property
    def num_answers(self):
        return self.comments.filter(author__is_staff=True).count()


class Comment(models.Model):

    class Meta:
        ordering = 'created',
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    content = models.TextField()
    
    def __str__(self):
        return f'{self.author} comment on {self.post}'


class Settings(models.Model):
    
    token = models.CharField(max_length=256, null=True)
    whitelist = models.TextField(null=True)

    def __str__(self):
        return 'configuration'

    @classmethod
    def get(cls):
        return cls.objects.first()
