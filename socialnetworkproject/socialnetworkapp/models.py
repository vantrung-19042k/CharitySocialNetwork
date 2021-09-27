from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

from ckeditor.fields import RichTextField


class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/users/%Y/%m',
                               validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100, blank=True)
    content = RichTextField()
    liked = models.ManyToManyField(User, blank=True, related_name='likes')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='uploads/posts/%Y/%m',
                              validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=True)
    tags = models.ManyToManyField('Tag', related_name='post_tag', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def num_likes(self):
        return self.liked.all().count()

    def count_comments(self):
        return self.comment_set.all().count

    class Meta:
        ordering = ['-created_date']


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)


class Like(models.Model):
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"


class Comment(models.Model):
    content = models.TextField(max_length=300, null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)


class Report(models.Model):
    class Meta:
        unique_together = ('user_create_report', 'user_is_reported')

    reason = models.TextField(max_length=300, null=False)
    image = models.ImageField(upload_to='uploads/reports/%Y/%m',
                              validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=True)
    reported_date = models.DateTimeField(auto_now_add=True)

    user_create_report = models.ForeignKey(User, on_delete=models.SET_NULL,
                                           null=True, related_name='user_create_report')
    user_is_reported = models.ForeignKey(User, on_delete=models.SET_NULL,
                                         null=True, related_name='user_is_reported')


class AuctionItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300, blank=True, null=True)
    image = models.ImageField(upload_to='uploads/aution_items/%Y/%m',
                              validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=True)
    user_sell = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Transaction(models.Model):
    items = models.ForeignKey(AuctionItem, on_delete=models.CASCADE)

    transaction_date = models.DateTimeField(auto_now_add=True)
    started_price = models.FloatField(null=True, blank=True)
    last_price = models.FloatField(null=True, blank=True)

    user_buy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

