from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (TemplateView, ListView,
                                DetailView, CreateView, UpdateView, DeleteView)
from Blog.models import Post, Comment
from Blog.forms import PostForm, CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Create your views here.

class AboutView(TemplateView):
    template_name = 'blog/about.html'

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    template_name = 'blog/post_form.html'

    form_class = PostForm

    model = Post

    success_url = reverse_lazy('post_list')

class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    template_name = 'blog/post_form.html'

    form_class = PostForm

    model = Post

    success_url = reverse_lazy('post_list')

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_draft_list')
    template_name = 'blog/post_confirm_delete.html'

class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    template_name = 'blog/post_draft.html'

    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')


#################################
#########Login required##########
#################################

@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()

    return redirect('post_detail',pk=pk)

@login_required
def add_comment_to_post(request,pk):
    post = get_object_or_404(Post,pk=pk)

    if request.method == 'POST':

        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():

            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail',pk=comment.post.pk)

    else:
        comment_form = CommentForm()
    return render(request,'blog/comment_form.html',{'form':comment_form})

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()

    return redirect('post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    comment.delete()

    return redirect('post_detail',pk=post_pk)
