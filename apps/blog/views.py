from django.shortcuts import render
from django.views.generic import ListView, DetailView

class PostListView(ListView):
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        return []

class PostDetailView(DetailView):
    template_name = 'blog/post_detail.html'
    
class CategoryPostsView(ListView):
    template_name = 'blog/category_posts.html'
    
class TagPostsView(ListView):
    template_name = 'blog/tag_posts.html'