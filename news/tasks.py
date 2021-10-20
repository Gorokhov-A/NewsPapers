from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

#models
from .models import Categories, Post

#time
from datetime import datetime
from datetime import timedelta

@shared_task
def sendfNewPost(category_id, instance_id):
    category = Categories.objects.get(id = category_id)
    post = Post.objects.get(id = instance_id)
    for user in category.subscribers.all():
        html_content = render_to_string(
                    'newPublication.html',
                    {
                        'category_info': category,
                        'post_id' : instance_id,
                        'post': post, 
                        'user' : user
                    }
                )
            
        msg = EmailMultiAlternatives(
                    subject = f'{post.post_title}',
                    body = html_content,
                    from_email = 'artiom199821zxc@gmail.com',
                    to = [f'{user.email}']
                )
        msg.attach_alternative(html_content, "text/html")

        msg.send()

@shared_task
def sendWeeklyPostUp():
    delta_last_week = datetime.now() - timedelta(days = 7)
    categories = Categories.objects.all()
    posts_dict = {}
    for category in categories:

        for user in category.subscribers.all():

            for post in Post.objects.filter(category = category, post_date__gte = delta_last_week):

                if user not in posts_dict:
                    posts_dict[user] = [post]

                elif post not in posts_dict[user]:
                    posts_dict[user].append(post)
    
    for user in posts_dict.keys():
        html_content = render_to_string(
            'weeklyupdating.html',
            {
                'user' : user,
                'posts' : posts_dict[user]
            }
            )

        msg = EmailMultiAlternatives(
            subject = f'Last week news updating',
            body = html_content,
            from_email = 'artiom199821zxc@gmail.com',
                to = [f'{user.email}']
            )
        msg.attach_alternative(html_content, "text/html")

        msg.send()

    