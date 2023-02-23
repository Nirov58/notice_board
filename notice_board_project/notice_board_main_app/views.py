from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from guardian.mixins import PermissionRequiredMixin

from .models import Post, Response, Category
from .forms import PostForm, ResponseForm
from .filters import PostFilter


class PostList(ListView):
    model = Post
    ordering = '-date'
    template_name = 'post_list.html'
    context_object_name = 'post_list'
    filterset = None
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostItem(DetailView):
    model = Post
    template_name = 'post_item.html'
    context_object_name = 'post_item'


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        return super().form_valid(form)


class PostEdit(PermissionRequiredMixin, UpdateView):
    permission_required = 'notice_board_main_app.change_post'
    return_403 = True
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    context_object_name = 'post_edit'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'notice_board_main_app.delete_post'
    return_403 = True
    raise_exception = True
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class PostRespond(LoginRequiredMixin, CreateView):
    form_class = ResponseForm
    model = Response
    template_name = 'post_respond.html'

    def form_valid(self, form):
        response = form.save(commit=False)
        target_id = self.request.path_info.split('/')[-3]
        response.target = Post.objects.get(pk=target_id)
        response.author = self.request.user
        return super().form_valid(form)


class PostsInCategory(PostList):
    template_name = 'post_category.html'
    context_object_name = 'post_category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_id'] = self.request.path_info.split('/')[-2]
        context['category'] = Category.objects.get(pk=context['category_id'])
        print(context['category'])
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(pk=pk)
    category.subscribers.add(user)
    return redirect('../')


@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(pk=pk)
    category.subscribers.remove(user)
    return redirect('../')
