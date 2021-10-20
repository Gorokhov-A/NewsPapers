from django.db.models.signals import m2m_changed, post_save
from django.template.loader import render_to_string
from django.dispatch import receiver

#celery tasks
from .tasks import sendfNewPost

#models
from .models import Post


@receiver(m2m_changed, sender = Post.category.through)
def notifyUsers(sender, instance, **kwargs):
    post_info = instance.category.all()
    for category in post_info:

        if category.subscribers:
            sendfNewPost.delay(category.pk, instance.pk)