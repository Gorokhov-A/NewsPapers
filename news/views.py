from django.db.models.deletion import CASCADE
from django.http import request
from django.views.generic import ListView, CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.core.cache import cache

from allauth.account.forms import ChangePasswordForm

from .filters import PostFilter
from .models import Post, Categories
from .forms import PostForm, ProfileUpadteForm


# Create your views here.

class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-post_date')
    paginate_by =  5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['categories'] = Categories.objects.all()
        context['form'] = PostForm()

        return context

class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    #queryset = Post.objects.order_by('-post_date')
    ordering = ['-post_date']
    paginate_by = 1

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())
            
    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['filter'] = self.get_filter()
        return context

class PostDetail(LoginRequiredMixin, DetailView):
    template_name = 'post.html'
    queryset = Post.objects.all()

    def get_object(self):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset = self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        print(obj)
        return obj

@login_required
def upgradeMe(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect('/posts')

class PostCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'create.html'
    form_class = PostForm
    permission_required = ('news.add_post',)

class PostUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'edit.html'
    form_class = PostForm
    permission_required = ('news.change_post',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk = id)

class PostDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/posts/'
    permission_required = ('news.delete_post',)

class UserUpdateView(UpdateView):
    template_name = 'profile.html'
    form_class = ProfileUpadteForm

    def get_object(self, **kwargs):
        current_user = self.kwargs.get('pk')
        return User.objects.get(pk = current_user)

class PasswordUpdateView(UpdateView):
    template_name = 'pwdchage.html'
    queryset = User.objects.all()
    form_class = ChangePasswordForm

class CatigoriesView(ListView):
    template_name = 'categories.html'
    context_object_name = 'categories'
    queryset = Categories.objects.all()

@login_required
def subscribe(request, **kwargs):
    pk = kwargs.get('pk')
    category = Categories.objects.get(id = pk)
    category_sub = Categories.objects.filter(subscribers = request.user)
    if not category in category_sub:
        category.subscribers.add(request.user )
    return redirect('/posts/categories/')

@login_required
def unsubscribe(request, **kwargs):
    pk = kwargs.get('pk')
    category = Categories.objects.get(pk = pk)
    category.subscribers.remove(request.user)
    print('unsubscribe')
    return redirect('/posts/categories/')
