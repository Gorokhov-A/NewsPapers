
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.decorators.cache import cache_page
from .views import PostList, PostDetail, PostSearch, PostCreateView, PostDeleteView, PostUpdateView, UserUpdateView, CatigoriesView, upgradeMe, subscribe, unsubscribe

urlpatterns = [
    path('', PostList.as_view(), name = 'posts_list'),
    path('categories/', CatigoriesView.as_view(), name = 'categories_list'),
    path('search/', PostSearch.as_view(), name = 'post_search'),
    path('<int:pk>',PostDetail.as_view(), name = 'post_detail'),
    path('create/', PostCreateView.as_view(), name = 'post_create'),
    path('update/<int:pk>/', PostUpdateView.as_view(), name = 'post_update'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name = 'post_delete'),
    path('upgrade/', upgradeMe, name = 'upgrade'),
    path('subscribe/<int:pk>', subscribe, name = 'subscribe'),
    path('unsubscribe/<int:pk>', unsubscribe, name = 'unsubscribe'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('profile/<int:pk>', UserUpdateView.as_view(), name = 'user_profile'),
]