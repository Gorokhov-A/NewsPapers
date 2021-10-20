from django_filters import FilterSet
import django_filters
from .models import Post
from django.forms import DateInput

class PostFilter(FilterSet):

    title = django_filters.CharFilter(field_name = 'post_title', lookup_expr = 'icontains', label = 'Title')
    date = django_filters.DateFilter(field_name = 'post_date', widget=DateInput(attrs = {'type' : 'date'}), lookup_expr = 'lt', label = 'Less this date')

    class Meta:
        model = Post
        fields = {
            'author_id__user_id__username' : ['icontains'],
            'category' : ['exact']
        }


# PostCategory.objects.filter(category__subscribers__username = 'artiom').values()  