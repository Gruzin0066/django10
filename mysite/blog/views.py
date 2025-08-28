from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import AddPostForm
from .models import Category, Post, PostTags


# Create your views here.
class HomePageView(TemplateView):
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Home Page'
        return context


class AboutPageView(LoginRequiredMixin,TemplateView):
    template_name = 'blog/about.html'
    login_url = '/users/login/'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, '🔐 Пожалуйста, авторизуйтесь для доступа к этой странице.')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'About Page'
        return context

class CategoryListView(ListView):
    # model = Category
    template_name = 'blog/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категории'
        return context



class CategoryPageView(ListView):
    # model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    slug_url_kwarg = 'slug'
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class PostPageView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Post.objects.get(slug=self.kwargs['slug'])
        return context


class PostByTagsListView(ListView):
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 5
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'], is_published=True)

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['title'] = PostTags.objects.get(slug=self.kwargs['slug'])
        return contex

def show_tags(request, slug):
    tags = PostTags.objects.all()
    tag = get_object_or_404(PostTags, slug=slug)
    posts = tag.tags.filter(is_published=True).prefetch_related('category')
    context = {
        'tag': tag,
        'posts': posts,
        'tags': tags,
        'title': tag.tag
    }
    return render(request, 'blog/home.html', context=context)


class AddPostView(LoginRequiredMixin, CreateView):
    # model = Post
    form_class = AddPostForm
    template_name = 'blog/add_post.html'
    # success_url = reverse_lazy('index')  # замени на свой URL

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, '🔐 Пожалуйста, авторизуйтесь для доступа к этой странице.')
        return super().dispatch(request, *args, **kwargs)


class PostEditPage(LoginRequiredMixin, UpdateView):
    model = Post
    fields = '__all__'
    template_name = 'blog/add_post.html'
    success_url = reverse_lazy('index')
    extra_context = {
        'title': 'Редактирование страницы'
    }

class PostDeletePage(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('index')
