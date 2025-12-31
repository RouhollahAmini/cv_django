from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # لیست مقالات
    path('', views.PostListView.as_view(), name='post_list'),
    
    # جزئیات مقاله
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    
    # مقالات یک دسته بندی
    path('category/<slug:slug>/', views.CategoryPostsView.as_view(), name='category'),
    
    # مقالات یک تگ
    path('tag/<slug:slug>/', views.TagPostsView.as_view(), name='tag'),
]