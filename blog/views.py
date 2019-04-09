from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# posts = [
#     {
#         'author': 'admin',
#         'title': 'first post',
#         'content': 'first post content',
#         'date_posted': 'April 1, 2019'
#     },
#     {
#         'author': 'john doe',
#         'title': 'second post',
#         'content': 'second post content',
#         'date_posted': 'April 2, 2019'
#     },
# ]


# Function-based views
def home(request):
    # return HttpResponse('<h1>Blog Home</h1>')
    # context = {
    #     'posts': posts
    # }
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context=context)


def about(request):
    # return HttpResponse('<h1>About Blog</h1>')
    return render(request, 'blog/about.html', context={'title': 'About Blog'})


# Class-based views (list views, detail views, create views, update views, delete views...)

class PostListView(ListView):
    model = Post
    # by default django looks for template at <app>/<model>_<viewtype>.html
    # which is blog/post_list.html
    # so we need to alter this behaviour
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted'] # ordering asc with minus sign
    paginate_by = 5 # paginations functionality



class PostDetailView(DetailView):
    # by default django looks for template at <app>/<model>_<viewtype>.html!
    # -> blog/post_detail.html
    model = Post


# to restrict access for unauthorized users we can use
# @method_decorator(login_required, name='dispatch') for class
# or mixins (must be placed as first argument in inheritance):
class PostCreateView(LoginRequiredMixin, CreateView):
    # by default django looks for template at <app>/<model>_<viewtype>.html!
    # -> blog/post_form.html
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        # every post has to have author
        form.instance.author = self.request.user
        return super().form_valid(form)


# to restrict updating posts the one is not owner use UserPassesTestMixin
# and override test_func() method
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # by default django looks for template at <app>/<model>_<viewtype>.html!
    # -> blog/post_form.html
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        # every post has to have author
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    # by default django looks for template at <app>/<model>_<viewtype>.html!
    # -> post_confurm_delete.html
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



class UserListView(ListView):
    model = Post
    # by default django looks for template at <app>/<model>_<viewtype>.html
    # which is blog/post_list.html
    # so we need to alter this behaviour
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5 # paginations functionality

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
