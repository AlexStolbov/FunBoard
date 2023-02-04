import logging
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostCreateForm, CommentCreateForm
from .models import Posts, Comments, PortalUser

logger_debug_one = logging.getLogger("debug_one")


class PostList(ListView):
    model = Posts
    template_name = 'posts_list.html'
    context_object_name = 'posts'
    # ToDo make paginate
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            logger_debug_one.info(f'post list {self.request.user}')
            context['portal_user'] = PortalUser.objects.get(user=self.request.user)
        return context


class PostDetail(LoginRequiredMixin, DetailView):
    """
    Просмотр статьи
    """
    model = Posts
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comments.objects.filter(
            post=self.object.id).filter(deleted=False).filter(approved=True)
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    model = Posts
    form_class = PostCreateForm
    template_name = 'post_create.html'
    success_url = '/posts/'

    def form_valid(self, form):
        """
        Заполняет автора у объявления
        """
        post = form.save(commit=False)
        post.author = PortalUser.objects.get(user=self.request.user)

        return super().form_valid(form)


class CommentCreate(LoginRequiredMixin, FormView):
    """
    Создание отклика
    """
    form_class = CommentCreateForm
    model = Comments
    template_name = 'post_comment.html'
    context_object_name = 'comment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = Posts.objects.get(pk=self.request.GET.get("post_pk"))
        return context

    def post(self, request, *args, **kwargs):
        self.create_comment()
        return redirect(f'/posts/{self.request.POST.get("post_pk")}')

    def create_comment(self):
        comment = Comments()
        comment.author = PortalUser.objects.get(user=self.request.user)
        comment.post = Posts.objects.get(pk=self.request.POST.get('post_pk'))
        comment.content = self.request.POST.get('content')
        comment.save()

    def form_valid(self, form):
        return super().form_valid(form)


class CommentApprove(LoginRequiredMixin, ListView):
    model = Comments
    template_name = 'comment_approve.html'
    context_object_name = 'comments'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(post=self.request.GET.get('post_pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = Posts.objects.get(pk=self.request.GET.get('post_pk'))
        return context


def comment_approve(request, *args, **kwargs):
    logger_debug_one.info(f'comment approve {kwargs}')
    comment = Comments.objects.get(pk=request.GET.get('comment_id'))
    comment.approved = True
    comment.approved_notice = True
    comment.deleted = False
    comment.save()
    return redirect(f'/posts/{comment.post.id}')


def comment_delete(request, *args, **kwargs):
    logger_debug_one.info(f'comment approve {kwargs}')
    comment = Comments.objects.get(pk=request.GET.get('comment_id'))
    comment.deleted = True
    comment.deleted_notice = True
    comment.save()
    return redirect(f'/posts/{comment.post.id}')


def subscribe_on(request, *args, **kwargs):
    if request.user.is_authenticated:
        subscribe_change(request.user, True)
    return redirect(f'/posts/')


def subscribe_off(request, *args, **kwargs):
    if request.user.is_authenticated:
        subscribe_change(request.user, False)
    return redirect(f'/posts/')


def subscribe_change(user, subscribe):
    portal_user = PortalUser.objects.get(user=user)
    portal_user.subscribers = subscribe
    portal_user.save()
