from django.core.management.base import BaseCommand, CommandError

#models
from news.models import Post, Categories

class Command(BaseCommand):
    help = 'Delete news in a specific category'
    requires_migrations_checks = True

    def handle(self, *args, **options):
        self.stdout.write('Do you really want to delete all news from a sepcificated category? Y/N')

        answer = input()

        if answer == 'Y':
            category_name = input('Enter the Category: ')
            category_object = Categories.objects.get(category = category_name)
            Post.objects.filter(category = category_object).delete()
            self.stdout.write(self.style.SUCCESS('Successfuly wiped posts'))
            return
        
        self.stdout.write(self.style.ERROR('Access denied'))
