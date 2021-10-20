from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group, User
from django.forms import ModelForm
from .models import Post
from django import forms
from django.core.mail import send_mail

class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['titile_state', 'post_title', 'post_text', 'author', 'category']

class ProfileUpadteForm(ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        
        widgets = {
            'username' : forms.TextInput(attrs={
                'class' : 'profile_update_username',
                'required': True,
                'label' : 'Username',
                'placeholder' : 'username',
            }),

            'first_name' : forms.TextInput(attrs={
                'class' : 'profile_update_first_name',
                'required': True,
                'label' : 'First name',
                'placeholder' : 'first name',
            }),

            'last_name' : forms.TextInput(attrs={
                'class' : 'profile_update_last_name',
                'required': True,
                'label' : 'last name',
                'placeholder' : 'last name',
            }),

            'email' : forms.EmailInput(attrs={
                'class' : 'profile_update_email',
                'required': False,
                'label' : 'Email',
                'placeholder' : 'email',
            }),            
        }

class BasicSignupForm(SignupForm):

    def save(self, request): #this method only executed if user are respected all points of signup form
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name = 'common') # we get object of basic group
        common_group.user_set.add(user)
        return user