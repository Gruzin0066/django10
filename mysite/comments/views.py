# comments/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.http import HttpResponse

# Правильные импорты
from .models import Comment
from .forms import CommentForm  # ← исправленный импорт
from blog.models import Post


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comments/add_comment.html'
    login_url = '/users/login/'  # явно указываем URL для входа
    redirect_field_name = 'next'  # чтобы вернуться обратно после входа

    def form_valid(self, form):
        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        form.instance.author = self.request.user
        form.instance.post = post
        messages.success(self.request, 'Комментарий успешно добавлен!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post', kwargs={'slug': self.kwargs['slug']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, slug=self.kwargs['slug'])
        return context


class PostCommentsListView(ListView):
    model = Comment
    template_name = 'comments/comments_list.html'
    context_object_name = 'comments'
    paginate_by = 10

    def get_queryset(self):
        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        return Comment.objects.filter(
            post=post,
            is_active=True
        ).select_related('author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, slug=self.kwargs['slug'])
        return context


# Функция для тестирования
def test_view(request):
    return HttpResponse("Test view works!")


def moderate_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            comment.is_active = True
            comment.save()
            messages.success(request, 'Комментарий одобрен')
        elif action == 'reject':
            comment.is_active = False
            comment.save()
            messages.success(request, 'Комментарий отклонен')
        elif action == 'delete':
            comment.delete()
            messages.success(request, 'Комментарий удален')
        return redirect('comments:moderation_list')

    return render(request, 'comments/moderate_comment.html', {'comment': comment})
