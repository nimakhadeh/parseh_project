from django.shortcuts import render, get_object_or_404
from .models import Post

def blog_list(request):
    posts = Post.objects.filter(is_published=True)
    context = {
        'posts': posts,
    }
    return render(request, 'blog/blog_list.html', context)

def blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    # افزایش تعداد بازدید
    post.views_count += 1
    post.save(update_fields=['views_count'])
    context = {
        'post': post,
    }
    return render(request, 'blog/blog_detail.html', context)
