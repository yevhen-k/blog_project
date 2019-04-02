from django.shortcuts import render
# from django.http import HttpResponse

posts = [
    {
        'author': 'admin',
        'title': 'first post',
        'content': 'first post content',
        'date_posted': 'April 1, 2019'
    },
    {
        'author': 'john doe',
        'title': 'second post',
        'content': 'second post content',
        'date_posted': 'April 2, 2019'
    },
]

def home(request):
    # return HttpResponse('<h1>Blog Home</h1>')
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context=context)


def about(request):
    # return HttpResponse('<h1>About Blog</h1>')
    return render(request, 'blog/about.html', context={'title': 'About Blog'})