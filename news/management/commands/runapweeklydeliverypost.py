import logging
 
from django.conf import settings
 
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

#models
from news.models import Post, Categories

#time
from datetime import datetime
from datetime import timedelta
 
 
logger = logging.getLogger(__name__)
 
 

def my_job():
    last_week = datetime.now() - timedelta(days = 7)
    posts = Post.objects.filter(post_date__gte = last_week)
    categories = Categories.objects.all()

    current_site = Site.objects.get_current()
    current_site.domain
    
    subscribers_dict = {}

    for post in posts:

        for category_ in post.category.all():

            for subscriber in category_.subscribers.all():
                
                if subscriber not in subscribers_dict:
                    subscribers_dict[subscriber] = [post]
                
                else:
                    subscribers_dict[subscriber].append(post)
    
    for user in subscribers_dict:
        html_content = render_to_string(
            'weeklyupdating.html',
            {
                    'domain' : current_site.domain,
                    'user' : user,
                    'posts' : subscribers_dict[user]
            }
        )

        msg = EmailMultiAlternatives(
            subject = f'Last week news updating',
            body = f'Hello {user} here is the latest news of this week {subscribers_dict[user]}',
            from_email = 'artiom199821zxc@gmail.com',
                to = [f'{user.email}']
            )
        msg.attach_alternative(html_content, "text/html")

        msg.send()

 
# функция которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)
 
 
class Command(BaseCommand):
    help = "Runs apscheduler."
 
    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        
        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),  # Тоже самое что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")
 
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )
 
        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")