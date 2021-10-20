from django.core.cache import cache
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields.related import ForeignKey, OneToOneField

class Author(models.Model):
    user_rating = models.FloatField(default = 0.0)
    user = models.OneToOneField(User, on_delete = models.CASCADE)

    def updateRating(self):
        posts_author = Post.objects.filter(author = self.user_id)
        rating_article = sum([r.post_rating * 3 for r in posts_author])
        print(rating_article)
        rating_comments = sum(r.comment_rating for r in Comments.objects.filter(user = self.user_id))
        print(rating_comments)

        likes_author_comment_sum = sum(r.comment_rating for r in Comments.objects.filter(post__in = posts_author))
        print(likes_author_comment_sum)
        self.user_rating = likes_author_comment_sum + rating_article + rating_comments
        print(self.user_rating)
        self.save()
    
    def __str__(self):
        return self.user.get_username()

class Categories(models.Model):
    category = models.CharField(max_length = 255, unique = True)
    subscribers = models.ManyToManyField(User)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'

    STATE = [
        (ARTICLE, 'article'),
        (NEWS, 'news'),
    ]

    titile_state = models.CharField(
        max_length = 2,
        choices = STATE,
        default = NEWS,
    )

    post_date = models.DateTimeField(auto_now_add = True)
    post_title = models.CharField(max_length = 255, default = 'Any title')
    post_text = models.TextField(default = 'Any text')
    post_rating = models.FloatField(default = 0.0)

    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    category = models.ManyToManyField(Categories, through = 'PostCategory')
    
    def postLike(self):
        self.post_rating += 1 if self.post_rating < 10.0 else 0.0
        self.save()

    def postDislike(self):
        self.post_rating -=1 if self.post_rating > 0 else 0.0
        self.save()
        
    def preview(self):
        return self.post_text[:124] + '...'

    def get_absolute_url(self):
        return f'/posts/{self.id}'

    def getDateTime(self):
        return self.post_date

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')


    def __str__(self):
        return f'{self.titile_state} : {self.post_title} : {self.post_text} : {self.post_date}'

class PostCategory(models.Model):
    category = models.ForeignKey(Categories, on_delete = models.CASCADE)
    post = models.ForeignKey(Post, on_delete = models.CASCADE)

class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    comment_text = models.TextField(default = 'Any comment')
    comment_datetime = models.DateTimeField(auto_now_add = True)
    comment_rating = models.FloatField(default = 0.0)

    def commentLike(self):
        self.comment_rating += 1 if self.comment_rating < 10.0 else 0.0
        self.save()
    
    def commentDislike(self):
        self.comment_rating -=1 if self.comment_rating > 0.0 else 0.0
        self.save()

    def __str__(self):
        return self.comment_text
